from Domain.Production import Production


class Grammar:
    def __init__(self, file_name):
        self.symbols = set()
        self.terminals = set()
        self.non_terminals = set()
        self.productions = []
        if file_name != "":
            self._create(file_name)

    def _create(self, file_name):
        # 1) read from file, get productions and symbols
        with open(file_name, "r") as f:
            self.non_terminals = set(f.readline().strip().split(" "))
            self.terminals = set(f.readline().strip().split(" "))
            # the symbols can be gotten by   terminals U non_terminals
            self.symbols = self.terminals.union(self.non_terminals)
            # get and number all the productions
            for line in f.readlines():
                lhs, rhss = line.split("->")
                lhs = lhs.strip()
                # check if LHS is a non-terminal
                if lhs in self.non_terminals:
                    rhss = rhss.split("|")
                    for rhs in rhss:
                        rhs = tuple(filter(lambda s: s != "", map(lambda s: s.strip(), rhs.split(" "))))
                        # check each element to be part of the alphabet
                        for elem in rhs:
                            if elem not in self.symbols:
                                raise Exception("ERROR: Component of RHS `{}` is not a symbol from the alphabet!".format(elem))
                        self.productions.append(Production(len(self.productions), lhs, rhs))
                else:
                    raise Exception("ERROR: LHS `{}` is not a non-terminal from the alphabet!".format(lhs))
        lhs = "S'"
        while lhs in self.non_terminals:
            lhs += "'"
        self.productions.insert(0, Production(-1, lhs, [self.productions[0].lhs]))
        self.non_terminals.add(lhs)

    def save(self):
        return " ".join(self.terminals) + "/*/" + " ".join(self.non_terminals)

    def load(self, txt):
        lines = txt.split("/*/")
        self.terminals = lines[0].split(" ")
        self.non_terminals = lines[1].split(" ")
        self.symbols = self.terminals.union(self.non_terminals)
