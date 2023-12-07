class Production:
    def __init__(self, nr, lhs, rhs=()):
        self.nr = nr
        self.lhs = lhs
        self.rhs = rhs

    def __eq__(self, other):
        return self.nr == other.nr

    def __repr__(self):
        return "({}){} -> {}".format(self.nr, self.lhs, " ".join(self.rhs))

    def __hash__(self):
        return self.nr

    def copy(self):
        return Production(self.nr, self.lhs, list(self.rhs))

    def save(self):
        return "{}/*/{}/*/{}".format(self.nr, self.lhs, "/;/".join(self.rhs))

    @staticmethod
    def load(txt):
        prod = Production(0, "", ())
        txt = txt.split("/*/")
        prod.nr = int(txt[0])
        prod.lhs = txt[1]
        prod.rhs = txt[2].split("/;/")
        return prod
