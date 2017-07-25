from credentials import credentials
import requests
import json
import csv
import io


class settings:
    login_url = 'https://trader.degiro.nl/login/secure/login'
    client_url = 'https://trader.degiro.nl/pa/secure/client'
    portfolio_csv_url = 'https://trader.degiro.nl/reporting_s/secure/v3/positionReport/csv'


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
        response = requests.get(settings.portfolio_csv_url + '?intAccount=%s&sessionId=%s&country=NL&lang=nl' % (self.accountid, self.jsessionid))
        return Portfolio(response.text)


class Portfolio:
    def __init__(self, csv_text):
        self.funds = []
        with io.StringIO(csv_text) as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['Product'] == 'CASH & CASH FUND (EUR)':
                    self.cash = row['Waarde in EUR']
                else:
                    self.funds.append(row)

    def get_money_amount(self):
        return self.cash

    def get_active_portfolio(self):
        converted = []
        for f in self.funds:
            converted.append({
                'fund': {
                    'currency': f['Lokale waarde'],
                    'name': f['Product'],
                    'isin': f['Symbool/ISIN'],
                },
                'totVal': dutch_float(f['Waarde in EUR']),
                'size': dutch_float(f['Aantal']),
            })

        return converted


def dutch_float(f):
    return float(f.replace(',', '.'))
