from __future__ import division
from main import trade
from degiro.interface import get_free_isins
from degiro.models import Funds, Fund, Portfolio, Orders
import random
from models import PriceList


class FakePositionRow(object):
    def __init__(self, fund, amount):
        self.fund = fund
        self.buy_price = fund.prices[-1].price
        self.size = amount / self.buy_price

    @property
    def profit(self):
        profit = self.fund.prices[-1].price / self.buy_price - 1
        return profit

    @property
    def totVal(self):
        return self.size * self.fund.prices[-1].price

    def __repr__(self):
        return "%f of %s" % (self.size, self.fund)


class FakeSession(object):
    def __init__(self, pricelist):
        self.free_space = 300
        self.portfolio = Portfolio()
        self.pricelist = pricelist

    def get_funds(self):
        isins = get_free_isins()
        funds = Funds()
        for isin in isins:
            currency = random.choice(['EUR', 'EUR', 'USD'])
            fund = Fund({
                'id': isin,
                'name': isin,
                'isin': isin,
                'currency': currency,
            })
            fund.free = True

            funds.add(fund)
        return funds

    def get_portfolio(self):
        pricelist.extend_with_prices(self.portfolio.funds)
        return self.portfolio

    def get_orders(self):
        return Orders()

    def get_free_space(self):
        return self.free_space

    def buy(self, fund, amount):
        self.free_space -= amount
        self.portfolio.append(FakePositionRow(fund, amount))

    def sell(self, position):
        value = position.totVal
        self.free_space += value
        position.size = 0

    def cancel(self, order):
        raise NotImplementedError()

    def total_value(self):
        return self.get_free_space() + sum([f.totVal for f in self.get_portfolio()])


class FakePriceList(PriceList):
    def __init__(self):
        self.cache = {}
        self.day = 0

    def get_prices_for_isin(self, isin):
        if isin not in self.cache:
            self.cache[isin] = super(FakePriceList, self).get_prices_for_isin(isin)
        return self.cache[isin][0:self.day]


pricelist = FakePriceList()
session = FakeSession(pricelist)
for i in range(-50, 0):
    print "day", i
    pricelist.day = i
    trade(session, pricelist)

print session.total_value()
