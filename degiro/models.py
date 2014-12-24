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

    def __repr__(self):
        return "%d of %s" % (self.size, self.fund)


class Fund(object):
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.isin = data['isin']

    def __repr__(self):
        return self.name


    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)
