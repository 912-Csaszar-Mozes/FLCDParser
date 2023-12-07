class State:
    def __init__(self, nr, items):
        self.nr = nr
        self.items = items

    def __eq__(self, other):
        for item in self.items:
            if not other.has_item(item):
                return False
        return True

    def __repr__(self):
        return "s{}:\t\n{}".format(self.nr, "\t\n".join([str(i) for i in self.items]))

    def has_item(self, item):
        for i in self.items:
            if i == item:
                return True
        return False

    def copy(self):
        return State(self.nr, [item.copy() for item in self.items])
