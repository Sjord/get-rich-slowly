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


for fund in funds:
    isin = fund.isin
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
    newprices = source.get_prices(start, stop, isin)
    data['prices'] = pricejoin(data['prices'], newprices)

    with open(fn, 'w') as f:
        json.dump(data, f)

