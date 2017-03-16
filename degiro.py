from credentials import credentials
import requests

class settings:
    login_url = 'https://www.degiro.eu/trading/secure/login'
    update_url = 'https://www.degiro.eu/trading/secure/v4/update/'


def login():
    data = {
        'username': credentials['username'],
        'password': credentials['password']
    }
    response = requests.post(settings.login_url, data)
    try:
        result = response.json()
    except ValueError:
        raise LoginFailed

    return Session(result['jsessionid'], result['account'])


class Session:
    def __init__(self, jsessionid, accountid):
        self.jsessionid = jsessionid
        self.accountid = accountid

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
        funds = self['portfolio']['value'][0]['value']
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
