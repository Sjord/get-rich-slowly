import json
from datetime import datetime


class PriceList(object):
    def get_prices_for_isin(self, isin):
        try:
            with open('data/%s.json' % isin) as fp:
                data = json.load(fp)
                return Prices(data['prices'])
        except IOError:
            return Prices([])

    def extend_with_prices(self, funds):
        for fund in funds:
            fund.prices = self.get_prices_for_isin(fund.isin)
        return funds


class Prices(list):
    def __init__(self, data):
        super(Prices, self).__init__([Price(i) for i in data])

    def last(self):
        return self[-1]


class Price(object):
    def __init__(self, data=None):
        if data:
            self.date = datetime.strptime(data['date'], '%Y-%m-%d').date()
            self.price = data['price']
