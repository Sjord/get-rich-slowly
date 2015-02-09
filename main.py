import degiro
import schemes
import models


min_amount = 110
sell_profit = 0.04


def determine_funds_to_sell(portfolio):
    to_sell = []
    for position in portfolio:
        mfund = models.Fund.load(position.fund.isin)
        advice = schemes.get_recent_advice(mfund)
        if advice == schemes.Advice.sell or position.profit > sell_profit:
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


def should_cancel_order(order):
    isin = order.fund.isin
    mfund = models.Fund.load(isin)
    advice = schemes.get_recent_advice(mfund)
    return (order.buy and advice != schemes.Advice.buy) or (order.sell and advice != schemes.Advice.sell)



session = degiro.login()
available_funds = session.get_funds()
portfolio = session.get_portfolio()
orders = session.get_orders()

sellable = [p for p in portfolio.active if p.fund not in orders.funds]

to_sell = determine_funds_to_sell(sellable)
for position in to_sell:
    print "Selling", position
    session.sell(position)

for order in orders:
    if should_cancel_order(order):
        print "Canceling order", order
        session.cancel(order)

money = session.get_free_space()
if money >= min_amount:
    buyable = available_funds.eur.free - portfolio.active.funds - orders.funds
    to_buy = determine_funds_to_buy(buyable)
    for fund in to_buy:
        try:
            amount = (min_amount + money / int(money / min_amount)) / 2
            print "Buying", fund, "for", amount
            session.buy(fund, amount)
            money -= amount

            if money < min_amount:
                break
        except degiro.DeGiroError as e:
            print e
