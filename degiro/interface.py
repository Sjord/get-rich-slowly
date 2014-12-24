import degiro.remote
import degiro.production
from degiro.models import PositionRow, Fund, Portfolio


def login():
    settings = degiro.production
    session = degiro.remote.DeGiro(settings).login()
    return Interface(session)


class Interface(object):
    def __init__(self, session):
        self.session = session

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
        return set([Fund(f) for f in self.session.get_funds()])
