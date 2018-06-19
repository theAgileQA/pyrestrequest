#!/usr/bin/env python

import os
import time

# signature library
from httpsigner import algorithm, signer
import cryptography.hazmat.backends
import cryptography.hazmat.primitives.serialization


# get env variable set to target url
client_key_id = os.environ.get("KEY_ID")
backend = cryptography.hazmat.backends.default_backend()
with open('/keys/oci_api_key.pem', mode='rb') as infile:
    apikey_pem = infile.read().strip()


def request_signer():
    private_key = cryptography.hazmat.primitives.serialization.load_pem_private_key(
        apikey_pem, None, backend)
    # create object for keys and algorithm
    default_signer = signer.DefaultRequestSigner({client_key_id: private_key}, algorithm.AlgorithmRSASHA256)
    req_signer = signer.KeyedRequestSigner(default_signer, client_key_id)
    return req_signer


def generate_headers():
    headers = {'Date': time.strftime('%a, %d %b %Y %H:%M:%S GMT', time.gmtime())}
    return headers
