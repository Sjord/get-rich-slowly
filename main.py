from degiro import DeGiro
import production
import json

def determine_funds_to_sell(portfolio):
    return []

def determine_funds_to_buy(funds):
    return []

session = DeGiro(production).login()
portfolio = session.get_portfolio()
to_sell = determine_funds_to_sell(portfolio)
for fund in to_sell:
    sell_fund(fund)

money = session.get_free_space()
print type(money), money
if money > 2:
    available_funds = session.get_funds()
    to_buy = determine_funds_to_buy(available_funds)
    for fund in to_buy:
        amount = 1 + money / 2
        buy_fund(fund, amount)
        money -= amount

        if money <= 2:
            break
