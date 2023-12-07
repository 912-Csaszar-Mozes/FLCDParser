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
        with open("InputFiles/" + file_name, "r") as f:
            # get and number all the productions
            for line in f.readlines():

                lhs, rhss = line.split("->")
                lhs = lhs.strip()
                # add left hand side to non-terminals and symbols
                self.symbols.add(lhs)
                self.non_terminals.add(lhs)
                rhss = rhss.split("|")
                for rhs in rhss:
                    rhs = tuple(filter(lambda s: s != "", map(lambda s: s.strip(), rhs.split(" "))))
                    self.productions.append(Production(len(self.productions), lhs, rhs))
                    # add all symbols from right hand side to symbols
                    for s in rhs:
                        self.symbols.add(s)
        # the terminals can be gotten by symbols \ non_terminals
        self.terminals = self.symbols.difference(self.non_terminals)
