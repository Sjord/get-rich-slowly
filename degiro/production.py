from credentials import credentials

login_url = 'https://www.degiro.nl/login/secure/j_spring_security_check'
logout_url = 'https://www.degiro.nl/secure/j_spring_security_logout'
funds_url = 'https://www.degiro.nl/secure/v3/funds?iDisplayStart=0&iDisplayLength=1000'
total_portfolio_url = 'https://www.degiro.nl/secure/v3/update?totalPortfolio=0'
portfolio_url = 'https://www.degiro.nl/secure/v3/update?portfolio=0'
buy_url = 'https://www.degiro.nl/secure/v3/fundorder/send'
orders_url = 'https://www.degiro.nl/secure/v3/update?orders=0'
cancel_order_url = 'https://www.degiro.nl/secure/v3/order/%s/delete'
