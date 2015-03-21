from unittest2 import TestCase
from mock import Mock
from degiro.models import Funds, Fund


class FundsTest(TestCase):
    def test_free(self):
        funds = Funds([
            Mock(free=True),
            Mock(free=False),
        ])
        self.assertEquals(len(funds.free), 1)

    def test_eur(self):
        funds = Funds([
            Mock(currency='EUR'),
            Mock(currency='GBP'),
        ])
        self.assertEquals(len(funds.eur), 1)
