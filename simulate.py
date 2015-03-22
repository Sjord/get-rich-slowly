from __future__ import division
from main import trade
from degiro.interface import get_free_isins
from degiro.models import Funds, Fund, Portfolio, Orders, Order
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
        self.cash = 350
        self.portfolio = Portfolio()
        self.pricelist = pricelist
        self.orders = Orders()

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
        self.pricelist.extend_with_prices(self.portfolio.funds)
        return self.portfolio

    def get_orders(self):
        return self.orders

    def get_free_space(self):
        return self.cash - sum([o.amount for o in self.orders if o.buy])

    def buy(self, fund, amount):
        order = Order({'buysell': 'B', 'id': random.randrange(1E10)})
        order.fund = fund
        order.amount = amount
        order.size = amount / fund.prices[-1].price
        self.orders.append(order)

    def sell(self, position):
        order = Order({'buysell': 'S', 'id': random.randrange(1E10)})
        order.fund = position.fund
        self.orders.append(order)

    def cancel(self, order):
        self.orders.remove(order)

    def _execute_orders(self, orders):
        for order in orders:
            if order.buy:
                self.cash -= order.amount
                self.portfolio.append(FakePositionRow(order.fund, order.amount))
            else:
                position = [pos for pos in self.get_portfolio() if pos.fund == order.fund][0]
                value = position.totVal
                self.cash += value
                position.size = 0

    def execute_some_orders(self):
        to_execute = [o for o in self.orders if random.random() <= 0.3]
        self._execute_orders(to_execute)

        left = [o for o in self.orders if o not in to_execute]
        self.orders = Orders(left)

    def total_value(self):
        return self.cash + sum([f.totVal for f in self.get_portfolio()])


class FakePriceList(PriceList):
    def __init__(self):
        self.cache = {}
        self.day = 0

    def get_prices_for_isin(self, isin):
        if isin not in self.cache:
            self.cache[isin] = super(FakePriceList, self).get_prices_for_isin(isin)
        return self.cache[isin][0:self.day]


def simulate(pricelist, session):
    for i in range(-400, 0):
        session.execute_some_orders()
        pricelist.day = i
        trade(session, pricelist)
    return session.total_value()


if __name__ == "__main__":
    values = []
    pricelist = FakePriceList()
    for i in range(0, 20):
        session = FakeSession(pricelist)
        value = simulate(pricelist, session)
        values.append(value)
        print "Avg:", sum(values) / len(values)
