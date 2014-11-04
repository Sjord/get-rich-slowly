import requests
import json


class DeGiro(object):
    def __init__(self, settings):
        self.settings = settings

    def login(self):
        settings = self.settings
        data = {
            'j_username': settings.credentials['username'],
            'j_password': settings.credentials['password']
        }
        s = requests.Session()
        response = s.post(settings.login_url, data)
        if '/secure/v3' not in response.url:
            raise LoginFailed

        return Session(s, settings)


def from_json(content):
    return DeGiroDict(json.loads(content))


class DeGiroError(RuntimeError):
    pass


class Session(object):
    def __init__(self, rsession, settings):
        self.rsession = rsession
        self.settings = settings

    def logout(self):
        self.rsession.get(self.settings.logout_url)

    def get_funds(self):
        r = self.rsession.get(self.settings.funds_url)
        data = json.loads(r.content)
        return data['rows']

    def get_free_space(self):
        r = self.rsession.get(self.settings.total_portfolio_url)
        total_portfolio = from_json(r.content)
        return total_portfolio['totalPortfolio']['value']['freeSpace']

    def get_portfolio(self):
        r = self.rsession.get(self.settings.portfolio_url)
        portfolio = from_json(r.content)
        return portfolio['portfolio']['value']['conttype'][0]['positionrow']

    def buy(self, productId, amount):
        r = self.rsession.post(self.settings.buy_url, data={
            'product': productId,
            'type': 1,
            'buysell': 0,
            'sumOrParticiaptions': 0,
            'sum': amount,
            'participations': ''
        })

        # Error:
        # {"status":1,"message":"From trading system: rejected order because order violates internal account(1016257) spending limit. Order worst case execution value (including estimated fee) is 1.3 EUR and spending limit is 0 EUR","errorMessages":null}
        # Goed:
        # {"status":0,"message":"","errorMessages":null}

        response = json.loads(r.content)
        if response['status']:
            raise DeGiroError(response['message'])

    def sell(self, productId, participations):
        r = self.rsession.post(self.settings.buy_url, data={
            'product': productId,
            'type': 2,
            'buysell': 1,
            'sumOrParticiaptions': 1,
            'sum': '',
            'participations': participations
        })

        # Error:
        # {"status":1,"message":"From trading system: rejected order because order violates internal account(1016257) spending limit. Order worst case execution value (including estimated fee) is 1.3 EUR and spending limit is 0 EUR","errorMessages":null}
        # Goed:
        # {"status":0,"message":"","errorMessages":null}

        response = json.loads(r.content)
        if response['status']:
            raise DeGiroError(response['message'])


class DeGiroDict(object):
    def __init__(self, data):
        self.data = data

    def _wrap(self, data):
        if isinstance(data, list) or isinstance(data, dict):
            return DeGiroDict(data)
        return data

    def __getitem__(self, key):
        if key == 0 and self.is_dict_list():
            return self

        try:
            return self._wrap(self.data[key])
        except KeyError:
            if self.data['name'] == key:
                return self._wrap(self.data['value'])
        except TypeError:
            data = [item['value'] for item in self.data if item['name'] == key]
            if len(data) == 1:
                return self._wrap(data[0])
            return self._wrap(data)

    def __repr__(self):
        return repr(self.data)

    def __iter__(self):
        if (self.is_dict_list()):
            yield DeGiroDict(self.data)
        else:
            for item in self.data:
                yield DeGiroDict(item)

    def __len__(self):
        if self.is_dict_list():
            return 1
        else:
            return len(self.data)

    def is_dict_list(self):
        if not isinstance(self.data, list):
            return False

        for item in self.data:
            if 'name' not in item or 'value' not in item:
                return False

        return True


class DeGiroInterfaceError(StandardError):
    pass


class LoginFailed(DeGiroInterfaceError):
    pass
