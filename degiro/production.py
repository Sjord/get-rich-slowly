from credentials import credentials

login_url = 'https://trader.degiro.nl/login/secure/j_spring_security_check'
logout_url = 'https://trader.degiro.nl/a/secure/j_spring_security_logout'
funds_url = 'https://www.degiro.eu/products2/secure/v3/funds?iDisplayStart=0&iDisplayLength=1000'
total_portfolio_url = 'https://trader.degiro.nl/trading/secure/v4/update/{accountid};jsessionid={jsessionid}?totalPortfolio=0'
portfolio_url = 'https://trader.degiro.nl/trading/secure/v4/update/{accountid};jsessionid={jsessionid}?portfolio=0'
buy_url = 'https://trader.degiro.nl/a/secure/v3/fundorder/send'
orders_url = 'https://trader.degiro.nl/a/secure/v3/update?orders=0'
cancel_order_url = 'https://trader.degiro.nl/a/secure/v3/order/%s/delete'

