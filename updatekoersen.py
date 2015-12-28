from webkoersen import KoersenSource
import degiro 
import json
from datetime import date, datetime, timedelta

session = degiro.login()
funds = session.get_funds()
session.logout()

source = KoersenSource()

def pricejoin(old, new):
    all_prices = old + new
    all_prices.sort(key=lambda x: x['date'])
    return all_prices

def to_date(date_str):
    return datetime.strptime(date_str, '%Y-%m-%d').date()

def last_date(data):
    try:
        return to_date(data['prices'][-1]['date']) + timedelta(days=1)
    except (KeyError, AttributeError, IndexError):
        return None


get_isins = [
    'LU0376438312',  # BlackRock Global Funds World Technology Fund D
    'LU0976192475',  # F & C Portfolios Fund F&C European SmallCap R (EUR)
    'LU0995140356',  # Henderson Gartmore Fund Pan European Smaller Companies H
    'LU0837973634',  # Aberdeen Global Emerging Markets Infrastructure Eq. Fd E2
]

for fund in funds:
    isin = fund.isin
    if isin not in get_isins:
        continue
    print isin
    fn = 'data/%s.json' % isin

    try:
        with open(fn) as f:
            data = json.load(f)
    except IOError:
        data = {}

    try:
        data['prices']
    except KeyError:
        data['prices'] = []

    data.update(fund.__dict__)
    start = last_date(data) or '2012-01-01'
    stop = date.today()
    try:
        newprices = source.get_prices(start, stop, isin)
    except IOError:
        newprices = source.get_prices(start, stop, isin)

    data['prices'] = pricejoin(data['prices'], newprices)

    with open(fn, 'w') as f:
        json.dump(data, f)

