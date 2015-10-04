import degiro
import schemes
import models
import log


min_amount = 110


def determine_funds_to_sell(portfolio):
    to_sell = []
    for position in portfolio:
        advice = schemes.get_recent_advice(position.fund)
        if advice == schemes.Advice.sell:
            to_sell.append(position)

    return to_sell


def determine_funds_to_buy(funds):
    buyfunds = [f for f in funds if schemes.get_recent_advice(f) == schemes.Advice.buy]
    if len(buyfunds) > 1:
        buyfunds.sort(key=schemes.predict_profit)
        buyfunds = buyfunds[-3:]

    return buyfunds


def should_cancel_order(order):
    advice = schemes.get_recent_advice(order.fund)
    return (order.buy and advice != schemes.Advice.buy) or (order.sell and advice != schemes.Advice.sell)


def trade(session, pricelist):
    available_funds = session.get_funds()
    pricelist.extend_with_prices(available_funds)

    money = session.get_money_amount()
    portfolio = session.get_portfolio()
    log.write_portfolio(portfolio)
    log.write_money_amount(money)
    return
    pricelist.extend_with_prices(portfolio.funds)

    orders = session.get_orders()
    pricelist.extend_with_prices(orders.funds)

    sellable = [p for p in portfolio.active if p.fund not in orders.funds]

    to_sell = determine_funds_to_sell(sellable)
    for position in to_sell:
        print "Selling", position
        session.sell(position)

    for order in orders:
        if should_cancel_order(order):
            print "Canceling order", order
            session.cancel(order)

    freeSpace = money.freeSpace
    if freeSpace >= min_amount:
        buyable = available_funds.eur.free - portfolio.active.funds - orders.funds
        to_buy = determine_funds_to_buy(buyable)
        for fund in to_buy:
            try:
                amount = (min_amount + freeSpace / int(freeSpace / min_amount)) / 2
                print "Buying", fund, "for", amount
                session.buy(fund, amount)
                freeSpace -= amount

                if freeSpace < min_amount:
                    break
            except degiro.DeGiroError as e:
                print e


if __name__ == "__main__":
    session = degiro.login()
    pricelist = models.PriceList()
    trade(session, pricelist)
