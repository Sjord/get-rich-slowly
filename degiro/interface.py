import degiro.remote
import degiro.production
from degiro.models import PositionRow, Fund, Portfolio, Orders, Order, Funds


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
            self.funds = self._really_get_funds()
        return self.funds

    def _really_get_funds(self):
        funds = Funds()
        free_isins = get_free_isins()
        for fdata in self.session.get_funds():
            fund = Fund(fdata)
            fund.free = fund.isin in free_isins
            funds.add(fund)
        return funds

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


def get_free_isins():
    isins = []
    with open('docs/DEGIRO_Beleggingsfondsen_Kernselectie.txt') as fp:
        for line in fp:
            (isin, rest) = line.split(' ', 1)
            if len(isin) == 12:
                isins.append(isin)
    return isins
