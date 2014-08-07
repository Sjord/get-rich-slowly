from degiro import DeGiro
import production
import json

degiro = DeGiro(production)
session = degiro.login()
print json.dumps(session.get_funds())
session.logout()
