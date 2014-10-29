from degiro import DeGiro
import production
import json
import schemes
import models

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


def determine_funds_to_buy(funds):
    isins = [f['isin'] for f in funds]
    mfunds = [models.Fund.load(isin) for isin in isins]
    buyfunds = [f for f in mfunds if schemes.get_recent_advice(f) == schemes.Advice.buy]
    if len(buyfunds) > 1:
        buyfunds.sort(key = schemes.predict_profit)
        return buyfunds[-2:]
    else:
        return buyfunds


session = DeGiro(production).login()
available_funds = session.get_funds()
portfolio = session.get_portfolio()

to_sell = determine_funds_to_sell(available_funds, portfolio)
for fund in to_sell:
    sell_fund(fund)

money = session.get_free_space()
if money > 2:
    to_buy = determine_funds_to_buy(available_funds)
    for fund in to_buy:
        amount = 1 + money / 2
        print "Buying", fund, "for", amount
        buy_fund(fund, amount)
        money -= amount

        if money <= 2:
            break
