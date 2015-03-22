class Portfolio(list):
    @property
    def funds(self):
        """Funds in all position rows"""
        return set([pr.fund for pr in self])

    @property
    def active(self):
        """A new portfolio with only position rows with non-zero size"""
        return Portfolio([pr for pr in self if pr.size])


class PositionRow(object):
    def __init__(self, data):
        self.size = data['size']
        self.totVal = data['totVal']
        self.pl = data['pl']

    @property
    def profit(self):
        return self.pl / self.totVal

    def __repr__(self):
        return "%f of %s" % (self.size, self.fund)


class Fund(object):
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.isin = data['isin']
        self.currency = data['currency']

    def __repr__(self):
        return self.name

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)


class Funds(set):
    @property
    def free(self):
        return Funds([f for f in self if f.free])

    @property
    def eur(self):
        return Funds([f for f in self if f.currency == 'EUR'])


class Order(object):
    def __init__(self, data):
        self.buy = data['buysell'] == 'B'
        self.sell = data['buysell'] == 'S'
        self.id = data['id']

    def __repr__(self):
        return "Order of %s" % (self.fund)

    def __eq__(self, other):
        return self.id == other.id


class Orders(list):
    @property
    def funds(self):
        return set([o.fund for o in self])
