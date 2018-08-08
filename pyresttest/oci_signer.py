#!/usr/bin/env python

# signature library
import cryptography.hazmat.backends
import cryptography.hazmat.primitives.serialization

import base64
import email.utils
import hashlib

import httpsig_cffi.sign
import requests
import six

# get env variable set to target url
backend = cryptography.hazmat.backends.default_backend()
with open('/keys/oci_api_key.pem', mode='rb') as infile:
    apikey_pem = infile.read().strip()


def request_signer(request, client_key_id):
    signature = SignedRequestAuth(client_key_id, apikey_pem)
    signed_request = signature.__call__(request)
    return signed_request


class SignedRequestAuth(requests.auth.AuthBase):
    """
    A requests auth instance that can be reused across requests
    """
    generic_headers = ["date", "(request-target)", "host"]
    body_headers = [
        "content-length",
        "content-type",
        "x-content-sha256",
    ]
    required_headers = {
        "get": generic_headers,
        "head": generic_headers,
        "delete": generic_headers,
        "put": generic_headers + body_headers,
        "post": generic_headers + body_headers
    }

    def __init__(self, *args):
        """
        Takes either 2 or 4 args. (key_id, private_key) or (tenancy_ocid, user_ocid, key_fingerprint, private_key)
        """
        if len(args) not in [2, 4]:
            raise SyntaxError("SignedRequestAuth.__init__ takes 2 or 4 args.")
        elif len(args) == 2:
            key_id = args[0]
            private_key = args[1]
        elif len(args) == 4:
            tenancy_ocid = args[0]
            user_ocid = args[1]
            key_fingerprint = args[2]
            private_key = args[3]
            key_id = "/".join([tenancy_ocid, user_ocid, key_fingerprint])

        self.signers = {}
        for method, headers in six.iteritems(self.required_headers):
            signer = httpsig_cffi.sign.HeaderSigner(
                key_id=key_id, secret=private_key, algorithm="rsa-sha256", headers=headers[:])
            use_host = "host" in headers
            self.signers[method] = (signer, use_host)

    def inject_missing_headers(self, request, sign_body):
        # Inject date, content-type, and host if missing
        request.headers.setdefault("date", email.utils.formatdate(usegmt=True))
        request.headers.setdefault("content-type", "application/json")
        request.headers.setdefault("host", six.moves.urllib.parse.urlparse(request.url).netloc)

        # Requests with a body need to send content-type,
        # content-length, and x-content-sha256
        if sign_body:
            body = request.body or ""
            if "x-content-sha256" not in request.headers:
                if isinstance(body, bytes):
                    body = body.decode("utf-8")
                m = hashlib.sha256(body.encode("utf-8"))
                base64digest = base64.b64encode(m.digest())
                base64string = base64digest.decode("utf-8")
                request.headers["x-content-sha256"] = base64string
            request.headers.setdefault("content-length", len(body))

    def __call__(self, request):
        verb = request.method.lower()
        # nothing to sign for options
        if verb == "options":
            return request
        signer, use_host = self.signers.get(verb, (None, None))
        if signer is None:
            raise ValueError("Don't know how to sign request verb {}".format(verb))

        # Inject body headers for put/post requests, date for all requests
        sign_body = verb in ["put", "post"]
        self.inject_missing_headers(request, sign_body=sign_body)

        if use_host:
            host = six.moves.urllib.parse.urlparse(request.url).netloc
        else:
            host = None

        signed_headers = signer.sign(request.headers, host=host, method=request.method, path=request.path_url)
        request.headers.update(signed_headers)
        return request
