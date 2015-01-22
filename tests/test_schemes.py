from schemes import predict_profit, Ema, Advice, get_recent_advice
from unittest2 import TestCase
from models import Fund, Price
import math


class TestPredictProfit(TestCase):
    def test_constant_fund(self):
        fund = get_fund(lambda x: 5)
        self.assertEquals(0, predict_profit(fund))

    def test_ema_values(self):
        fund = get_fund(lambda x: 5 + 5 * abs(math.sin(x)))
        (ema_short, ema_long) = get_ema(fund)
        self.assertAlmostEqual(ema_short, 8.105437, 5)
        self.assertAlmostEqual(ema_long, 8.122001, 5)

    def test_predict_profit_value(self):
        fund = get_fund(lambda x: x)
        profit = predict_profit(fund)
        self.assertAlmostEqual(profit, 14.959724, 5)

    def test_get_recent_advice_value(self):
        fund = get_fund(lambda x: x)
        self.assertEquals(Advice.buy, get_recent_advice(fund))

        fund = get_fund(lambda x: 10000-x)
        self.assertEquals(Advice.sell, get_recent_advice(fund))

        fund = get_fund(lambda x: 5)
        self.assertEquals(Advice.sell, get_recent_advice(fund))


def get_ema(fund):
    ema = Ema()
    ema.updateAll(fund.prices)
    return (ema.emaShort, ema.emaLong)


def get_fund(get_price):
    fund = Fund()
    fund.prices = []
    for i in range(1, 1000):
        p = Price()
        p.price = get_price(i)
        fund.prices.append(p)
    return fund
