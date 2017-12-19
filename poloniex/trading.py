"""
The Poloniex trading API client.
"""

import hashlib
import hmac

import requests


BASE_URL = 'https://poloniex.com/tradingApi'


class Trading(object):

    def __init__(self, key, secret):
        self._key = key
        self._secret = secret

    def _generate_signature(self, secret, message):
        signature = hmac.new(
            key=secret,
            msg=message,
            digestmod=hashlib.sha512
        )
        return signature.hexdigest()

    def _signed_request(self, command, params=None):
        params = params if params is not None else {}
        params.update({'command': command})
        response = requests.get(BASE_URL, params=params)
        return response.json()
