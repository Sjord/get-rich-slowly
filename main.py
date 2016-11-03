import degiro
import log
import json


if __name__ == "__main__":
    session = degiro.login()
    portfolio = session.get_portfolio()
    log.write_money_amount(portfolio.get_money_amount())
    log.write_portfolio(portfolio.get_active_portfolio())
