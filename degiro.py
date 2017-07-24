from credentials import credentials
import requests
import json

class settings:
    login_url = 'https://trader.degiro.nl/login/secure/login'
    client_url = 'https://trader.degiro.nl/pa/secure/client'
    update_url = 'https://trader.degiro.nl/trading_s/secure/v5/update/'


def login():
    data = json.dumps({
        'username': credentials['username'],
        'password': credentials['password']
    })
    response = requests.post(settings.login_url, data)
    result = response.json()
    session_id = result['sessionId']

    return Session(session_id)


class Session:
    def __init__(self, jsessionid):
        self.jsessionid = jsessionid
        self.accountid = self.get_account_id()

    def get_account_id(self):
        response = requests.get(settings.client_url + '?sessionId=%s' % self.jsessionid)
        result = response.json()
        return result['intAccount']

    def get_portfolio(self):
        response = requests.get(settings.update_url + '%s;jsessionid=%s' % (self.accountid, self.jsessionid), params={'portfolio': 0, 'totalPortfolio': 0})
        return Portfolio(response.json())


def convert_degiro_listdict(listdict):
    result = {}
    for item in listdict:
        name = item['name']
        try:
            value = item['value']
        except KeyError:
            value = None
        result[name] = value
    return result


class Portfolio(dict):
    def get_money_amount(self):
        return convert_degiro_listdict(self['totalPortfolio']['value'])

    def get_active_portfolio(self):
        funds = self['portfolio']['value']
        funds = [convert_degiro_listdict(f['value']) for f in funds]
        funds = [f for f in funds if f['size'] > 0]
        
        converted = []
        for f in funds:
            converted.append({
                'fund': {
                    'currency': f['currency'],
                    'name': f['product'],
                    'id': f['id'],
                },
                'totVal': f['value'],
                'size': f['size'],
            })

        return converted
