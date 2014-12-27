import degiro.remote
import degiro.production
from degiro.models import PositionRow, Fund, Portfolio, Orders, Order


def login():
    settings = degiro.production
    session = degiro.remote.DeGiro(settings).login()
    return Interface(session)


class Interface(object):
    def __init__(self, session):
        self.session = session
        self.funds = None

    def get_portfolio(self):
        funds = self.get_funds()
        portfolio = self.session.get_portfolio()
        rows = Portfolio()
        for p in portfolio:
            row = PositionRow(p)
            (row.fund,) = [f for f in funds if f.id == p['id']]
            rows.append(row)
        return rows

    def get_funds(self):
        if not self.funds:
            self.funds = set([Fund(f) for f in self.session.get_funds()])
        return self.funds

    def sell(self, position):
        return self.session.sell(position.fund.id, position.size)

    def buy(self, fund, amount):
        return self.session.buy(fund.id, amount)

    def get_free_space(self):
        return self.session.get_free_space()

    def get_orders(self):
        funds = self.get_funds()
        orders = self.session.get_orders()
        result = Orders()
        for o in orders:
            order = Order(o)
            (order.fund,) = [f for f in funds if f.id == o['productId']]
            result.append(order)
        return result

    def logout(self):
        self.session.logout()
        
    def cancel(self, order):
        self.session.cancel(order.id)
