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
        if not '/secure/v3' in response.url:
            raise LoginFailed

        return Session(s, settings)


def from_json(content):
    return DeGiroDict(json.loads(content))


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
        print total_portfolio.data
        return total_portfolio['totalPortfolio']['value']['freeSpace']

    def get_portfolio(self):
        r = self.rsession.get(self.settings.portfolio_url)
        portfolio = from_json(r.content)
        return portfolio['portfolio']['value']['conttype'][0]['positionrow']


class DeGiroDict(object):
    def __init__(self, data):
        self.data = data
    def __getitem__(self, key):
        if key == 0 and self.is_dict_list():
            return self

        try:
            return DeGiroDict(self.data[key])
        except KeyError:
            if self.data['name'] == key:
                return DeGiroDict(self.data['value'])
        except TypeError:
            data = [item['value'] for item in self.data if item['name'] == key]
            return DeGiroDict(data)
        
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
