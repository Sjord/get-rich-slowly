from mock import Mock
from unittest2 import TestCase
from degiro.interface import Interface


class InterfaceTest(TestCase):
    def setUp(self):
        session = Mock()
        session.get_portfolio.return_value = [{
            'id': '4998723',
            'size': 0.821,
            'totVal': 100.,
            'pl': 3.,
        }]
        session.get_funds.return_value = [{
            'id': '4998723',
            'isin': 'LI0837977205',
            'name': 'ABERDEEN GL-INDIA EQTY-X-2A',
            'currency': 'USD',
        }, {
            'id': '5003027',
            'name': 'ABERDEEN GL-INDIA EQTY-Y-2A',
            'isin': 'LU0837977544',
            'currency': 'EUR',
        }]

        self.interface = Interface(session)

    def test_get_portfolio_joins_funds_and_portfolio(self):
        portfolio = self.interface.get_portfolio()
        self.assertEquals(len(portfolio), 1)
        self.assertEquals(portfolio[0].fund.isin, 'LI0837977205')

    def test_easily_get_funds_not_in_portfolio(self):
        funds = self.interface.get_funds()
        portfolio = self.interface.get_portfolio()
        not_in_portfolio = funds - portfolio.active.funds
        self.assertEquals(len(not_in_portfolio), 1)
        self.assertEquals(not_in_portfolio.pop().id, '5003027')

    def test_free_data_is_added_to_funds(self):
        funds = self.interface.get_funds()
        non_free = [f for f in funds if f.isin == 'LI0837977205'][0]
        self.assertFalse(non_free.free)

        free = [f for f in funds if f.isin == 'LU0837977544'][0]
        self.assertTrue(free.free)
