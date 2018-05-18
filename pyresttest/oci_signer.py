#!/usr/bin/env python

""" REMEMBER THIS IS A HACK UNTIL I GET THE TIME TO FINISH IT!! """

from email.utils import formatdate
import os

# signature library
from httpsigner import algorithm, signer, util
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
import requests

# get env variable set to target url
client_key_id = os.environ.get("KEY_ID")


def signature_generator(mytest):
    path = mytest.url

    # headers to sign is not the default, it also includes the HOST
    headers = (util.Headers.DATE, util.LHDR_HOST, util.LHDR_REQUEST_TARGET)
    # load headers and req_signer into the constant KeyedRequestSigner class.
    keyed_signer = signer.KeyedRequestSigner(request_signer(), client_key_id, headers_to_sign=headers)
    # pull url out of config and put into request
    signature = requests.Request("GET", path, headers={"date": formatdate(usegmt=True)}).prepare()
    # use the keyed_signer to generate a request using the signature provided
    keyed_signer.sign_request(signature)
    return signature.headers


def request_signer():
    # load private pem file
    with open("keys/oci_api_key.pem".format(loc=os.getcwd()), "rb") as f:
        apikey_pem = serialization.load_pem_private_key(f.read(), None, backend=default_backend())
    # create object for keys and algorithm
    req_signer = signer.DefaultRequestSigner({client_key_id: apikey_pem}, algorithm.AlgorithmRSASHA256)

    return req_signer
