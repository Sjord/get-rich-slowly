import json
from datetime import datetime

class Fund(object):
    @classmethod
    def load(cls, isincode):
        with open('data/%s.json' % isincode) as fp:
            data = json.load(fp)
            self = cls()
            self.prices = Prices(data['prices'])
            return self


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
