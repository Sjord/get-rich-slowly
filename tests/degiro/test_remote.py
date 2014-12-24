from unittest2 import TestCase
from degiro.remote import DeGiroDict
import json


def load_fixture(name):
    with open('tests/fixtures/' + name) as fp:
        return json.load(fp)


class TestDeGiroDict(TestCase):
    def test_free_space(self):
        data = load_fixture('totalPortfolio.json')
        d = DeGiroDict(data)
        self.assertEquals(d['totalPortfolio']['totalPortfolio']['freeSpace'], 2.645)

    def test_single_portfolio_fund_name(self):
        data = load_fixture('portfolio-single.json')
        d = DeGiroDict(data)
        self.assertEquals(d['portfolio']['portfolio']['conttype']['positionrow'][0]['id'], "4998723")

    def test_multi_portfolio_fund_name(self):
        data = load_fixture('portfolio-multi.json')
        d = DeGiroDict(data)
        self.assertEquals(d['portfolio']['portfolio']['conttype']['positionrow'][0]['id'], "4998723")
        self.assertEquals(d['portfolio']['portfolio']['conttype']['positionrow'][1]['id'], "4999807")

    def test_looping_through_positionrows(self):
        data = load_fixture('portfolio-multi.json')
        d = DeGiroDict(data)
        ids = [positionrow['id'] for positionrow in d['portfolio']['portfolio']['conttype']['positionrow']]
        self.assertEquals(ids, ['4998723', '4999807'])

