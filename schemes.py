from __future__ import division
import sys


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
    shortDays = 44
    longDays = 55

    def _init(self, prices):
        self.emaShort = prices[0].price
        self.emaLong = prices[0].price

    def updateAll(self, prices):
        prices = prices[-350:]
        self._init(prices)
        for p in prices:
            lastAdvice = self.update(p)
        return lastAdvice

    def update(self, priceobj):
        price = priceobj.price
        alpha = 2/(self.shortDays + 1)
        self.emaShort = alpha * price + (1 - alpha) * self.emaShort

        alpha = 2/(self.longDays+1)
        self.emaLong = alpha * price + (1 - alpha) * self.emaLong

        return self.emaShort > self.emaLong


def predict_profit(fund):
    profit = 0
    bought = None
    multiplier = None

    if len(fund.prices) < 2:
        return 0

    ndays = min(len(fund.prices) - 1, 131)

    advisor = Ema()
    advisor.updateAll(fund.prices[0:-ndays])

    for i in range(0, ndays):
        p = fund.prices[i-ndays]
        advice = advisor.update(p)

        if advice == Advice.buy and not bought:
            bought = p.price
            multiplier = 100 / bought
        if advice == Advice.sell and bought:
            profit += (p.price - bought) * multiplier
            bought = None
            multiplier = None
    if bought:
        profit += (fund.prices[-1].price - bought) * multiplier
    return profit


def get_recent_advice(fund):
    if not fund.prices:
        return Advice.none
    advisor = Ema()
    advice = advisor.updateAll(fund.prices)
    return advice


if __name__ == "__main__":
    isins = sys.argv[1:]

    funds = [Fund.load(isin) for isin in isins]
    print sorted(funds, key=predict_profit)
