"""
The Poloniex public API client.
"""

import requests


BASE_URL = 'https://poloniex.com/public'
PER_SECOND_LIMIT = 6


class Public(object):

    def _request(self, command, params=None):
        params = params if params is not None else {}
        params.update({'command': command})
        response = requests.get(BASE_URL, params=params)
        return response.json()

    def ticker(self):
        return self._request(command='returnTicker')

    def volume_over_24_hours(self):
        return self._request(command='return24volume')

    def order_book(self, currency_pair='all', depth=None):
        params = {'currencyPair': currency_pair}
        if depth is not None:
            params.update({'depth': depth})
        return self._request(
            command='return',
            params=params
        )

    def trade_history(self, currency_pair='all', start=None, end=None):
        return self._request(
            command='returnTradeHistory',
            params={'currencyPair': currency_pair}
        )
