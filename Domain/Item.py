from Domain.Production import Production


class Item:
    def __init__(self, prod: Production, dot_pos):
        self.prod = prod
        self.dot_pos = dot_pos

    def symbol_after_dot(self):
        return self.prod.rhs[self.dot_pos] if self.dot_pos < len(self.prod.rhs) else None

    def move_right(self):
        if self.dot_pos < len(self.prod.rhs):
            self.dot_pos += 1

    def __eq__(self, other):
        return self.prod == other.prod and self.dot_pos == other.dot_pos

    def __repr__(self):
        return "({}){} -> {}.{}".format(self.prod.nr, self.prod.lhs, " ".join(self.prod.rhs[:self.dot_pos]), " "
                                        .join(self.prod.rhs[self.dot_pos:]))

    def __hash__(self):
        return self.prod.nr

    def copy(self):
        return Item(self.prod.copy(), self.dot_pos)