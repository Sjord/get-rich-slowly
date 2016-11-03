import json
from datetime import date


class PortfolioEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, date):
            return o.strftime("%Y-%m-%d")
        return {k: v for k, v in o.__dict__.iteritems() if k != 'prices'}


def write_portfolio(portfolio):
    key = date.today().strftime("%Y-%m-%d")
    try:
        f = open('data/portfolio_history.json', 'r+')
        log = json.load(f)
    except IOError:
        f = open('data/portfolio_history.json', 'w')
        log = {}

    log[key] = portfolio

    f.seek(0)
    json.dump(log, f, indent=4, cls=PortfolioEncoder)
    f.truncate()
    f.close()


def write_money_amount(money_amount):
    key = date.today().strftime("%Y-%m-%d")
    try:
        f = open('data/money_history.json', 'r+')
        log = json.load(f)
    except IOError:
        f = open('data/money_history.json', 'w')
        log = {}

    log[key] = money_amount

    f.seek(0)
    json.dump(log, f, indent=4)
    f.truncate()
    f.close()
