class Portfolio(list):
    @property
    def funds(self):
        return set([pr.fund for pr in self])


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
