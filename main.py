import degiro
import production
import schemes
import models


min_amount = 100


def determine_funds_to_sell(portfolio):
    to_sell = []
    for position in portfolio:
        mfund = models.Fund.load(position.fund.isin)
        advice = schemes.get_recent_advice(mfund)
        if advice == schemes.Advice.sell:
            to_sell.append(position)

    return to_sell


def determine_funds_to_buy(funds):
    isins = [f.isin for f in funds]
    mfunds = [models.Fund.load(isin) for isin in isins]
    buyfunds = [f for f in mfunds if schemes.get_recent_advice(f) == schemes.Advice.buy]
    if len(buyfunds) > 1:
        buyfunds.sort(key=schemes.predict_profit)
        buyfunds = buyfunds[-3:]

    buy_isins = [f.isin for f in buyfunds]
    return [f for f in funds if f.isin in buy_isins]


session = degiro.login()
available_funds = session.get_funds()
portfolio = session.get_portfolio()

to_sell = determine_funds_to_sell(portfolio.active)
for position in to_sell:
    print "Selling", position.fund.name
    session.sell(position)

money = session.get_free_space()
if money >= min_amount:
    to_buy = determine_funds_to_buy(available_funds - portfolio.active.funds)
    for fund in to_buy:
        try:
            amount = money / int(money / min_amount)
            print "Buying", fund, "for", amount
            session.buy(fund, amount)
            money -= amount

            if money < min_amount:
                break
        except degiro.DeGiroError as e:
            print e
