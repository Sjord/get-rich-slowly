from __future__ import division
import sys
from models import Fund


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

    def advise(self, fund):
        emaShort = fund.prices[0].price
        emaLong = fund.prices[0].price

        for price in [p.price for p in fund.prices]:
            alpha = 2/(self.shortDays + 1)
            emaShort = alpha * price + (1 - alpha) * emaShort

            alpha = 2/(self.longDays+1)
            emaLong = alpha * price + (1 - alpha) * emaLong

        if (emaShort > emaLong):
            return Advice.buy
        if (emaLong > emaShort):
            return Advice.sell
        return Advice.none


if __name__ == "__main__":
    isin = sys.argv[1]
    fund = Fund.load(isin)
    print Ema().advise(fund)
