from degiro import DeGiro, DeGiroError
import production
import schemes
import models


min_amount = 100


def determine_funds_to_sell(funds, portfolio):
    to_sell = []
    for pfund in portfolio:
        id = pfund['id']
        ffund = [fund for fund in funds if fund['id'] == id][0]
        isin = ffund['isin']

        mfund = models.Fund.load(isin)
        advice = schemes.get_recent_advice(mfund)
        if advice == schemes.Advice.sell:
            to_sell.append(pfund)

    return to_sell


def determine_funds_to_buy(funds, portfolio):
    portfolio_ids = [f['id'] for f in portfolio]
    funds = [f for f in funds if f['id'] not in portfolio_ids]
    isins = [f['isin'] for f in funds]
    mfunds = [models.Fund.load(isin) for isin in isins]
    buyfunds = [f for f in mfunds if schemes.get_recent_advice(f) == schemes.Advice.buy]
    if len(buyfunds) > 1:
        buyfunds.sort(key=schemes.predict_profit)
        buyfunds = buyfunds[-3:]

    buy_isins = [f.isin for f in buyfunds]
    return [f for f in funds if f['isin'] in buy_isins]


session = DeGiro(production).login()
available_funds = session.get_funds()
portfolio = session.get_portfolio()

to_sell = determine_funds_to_sell(available_funds, portfolio)
for fund in to_sell:
    print "Selling", fund['name'], fund['isin']
    session.sell(fund['id'], fund['size'])

money = session.get_free_space()
if money >= min_amount:
    to_buy = determine_funds_to_buy(available_funds, portfolio)
    for fund in to_buy:
        try:
            amount = money / int(money / min_amount)
            print "Buying", fund['name'], fund['isin'], "for", amount
            session.buy(fund['id'], amount)
            money -= amount

            if money < min_amount:
                break
        except DeGiroError as e:
            print e
