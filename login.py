import degiro
import json

session = degiro.login()
print session.get_orders()
