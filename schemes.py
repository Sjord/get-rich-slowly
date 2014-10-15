from __future__ import division
import sys
from models import Fund
import datetime


class Advice(object):
    buy = True
    sell = False
    none = None


class NeverBuy(object):
    def advise(self, fund):
        return Advice.none


class MonthlyBuy(object):
    def advise(self, fund):
        if fund.prices.last().date.month % 2 == 0:
            return Advice.buy
        else:
            return Advice.sell


class Ema(object):
    shortDays = 9
    longDays = 14

    def __init__(self, fund):
        self.emaShort = fund.prices[0].price
        self.emaLong = fund.prices[0].price

    def update(self, priceobj):
        price = priceobj.price
        alpha = 2/(self.shortDays + 1)
        self.emaShort = alpha * price + (1 - alpha) * self.emaShort

        alpha = 2/(self.longDays+1)
        self.emaLong = alpha * price + (1 - alpha) * self.emaLong

        if (self.emaShort > self.emaLong):
            return Advice.buy
        if (self.emaLong > self.emaShort):
            return Advice.sell
        return Advice.none


def predict_profit(fund):
    day = datetime.date.today() - datetime.timedelta(days=365)
    profit = 0
    bought = None

    advisor = Ema(fund)
    [advisor.update(p) for p in fund.prices[0:-365]]

    for i in range(0, 365):
        p = fund.prices[i-366]
        advice = advisor.update(p)

        if advice == Advice.buy and not bought:
            bought = p.price
        if advice == Advice.sell and bought:
            profit += p.price - bought
            bought = None
    if bought:
        profit += fund.prices[-1].price - bought
    return profit


if __name__ == "__main__":
    isin = sys.argv[1]

    fund = Fund.load(isin)
    print predict_profit(fund)
