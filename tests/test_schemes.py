from schemes import predict_profit
from unittest2 import TestCase
from models import Fund, Price

class TestPredictProfit(TestCase):
    def test_constant_fund(self):
        fund = Fund()
        fund.prices = []
        for i in range(1, 1000):
            p = Price()
            p.price = 5
            fund.prices.append(p)

        self.assertEquals(0, predict_profit(fund))
