from pickle import load, dumps

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


class TableElem:
    def __init__(self, action, goto):
        self.action = action
        self.goto = goto

    def __repr__(self):
        return self.action + ": " + str(self.goto)

    def save(self):
        goto_str = "/;/".join(["{}/;;/{}".format(key, self.goto[key]) for key in self.goto])
        return "{}/*/{}".format(self.action, goto_str)

    @staticmethod
    def load(txt):
        table_elem = TableElem("",{})
        txt = txt.split("/*/")
        table_elem.action = txt[0]
        if "s" in table_elem.action:
            for keyval in txt[1].split("/;/"):
                keyval = keyval.split("/;;/")
                table_elem.goto[keyval[0]] = int(keyval[1])
        return table_elem


class LR0Table:
    def closure(self, state):
        changed = True
        while changed:
            changed = False
            for item in state.items:
                symbol_after_dot = item.symbol_after_dot()
                if symbol_after_dot in self.non_terminals:
                    for prod in self.productions:
                        if prod.lhs == symbol_after_dot:
                            new_item = Item(prod, 0)
                            if not state.has_item(new_item):
                                state.items.append(new_item)
                                changed = True
        return state

    def goto(self, state, symbol):
        items = []
        for item in state.items:
            if item.symbol_after_dot() == symbol:
                new_item = item.copy()
                new_item.move_right()
                items.append(new_item)
        return self.closure(State(-1, items))

    def __init__(self, file_name):
        self.meta_data = {}
        self.symbols = set()
        self.terminals = set()
        self.non_terminals = set()
        self.productions = []
        self.states = []
        self.table = []
        if file_name != "":
            self.create(file_name)

    def state_pos(self, state):
        for i in range(len(self.states)):
            if self.states[i] == state:
                return i
        return -1

    def create(self, file_name):
        # 1) read from file, get productions and symbols
        with open(file_name, "r") as f:
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

        # 2) calculate states and closures
        gotos = {}
        self.states.append(self.closure(State(0, [Item(self.productions[0], 0)])))
        i = 0
        while i < len(self.states):
            state = self.states[i]
            for s in self.symbols:
                new_state = self.goto(state, s)
                if len(new_state.items) != 0:
                    state_pos = self.state_pos(new_state)
                    new_state.nr = len(self.states) if state_pos == -1 else state_pos
                    if state_pos == -1:
                        self.states.append(new_state)
                    if gotos.get(i) is not None:
                        gotos[i].append((s, new_state.nr))
                    else:
                        gotos[i] = [(s, new_state.nr)]
            i += 1

        # 3) fill in the table
        for i in range(len(self.states)):
            # see if it is reduce or accept
            action = ""
            state = self.states[i]
            table_elem = TableElem("", {})
            for item in state.items:
                if item.symbol_after_dot() is None:
                    if action == "":
                        if item.prod == self.productions[0]:
                            action = "a"
                        else:
                            action = "r " + str(item.prod.nr)
                    else:
                        raise Exception("ERROR with state {} at item {}; old action: {}".format(state, item, action))
            for goto in gotos.get(i, []):
                if action == "" or action == "s":
                    table_elem.goto[goto[0]] = goto[1]
                    action = "s"
                else:
                    raise Exception("ERROR with state {} at item {}; old action: {}".format(state, item, action))
            table_elem.action = action
            self.table.append(table_elem)
            print(self.table)

    def get_action(self, state_nr, symbol):
        # Return values: `s <state_nr>` shift to state with number state_nr
        #                `r <prod_nr>` reduce with production prod_nr
        #                `err` error with parsing
        if self.table[state_nr].action == "s":
            if self.table[state_nr].goto.get(symbol) is not None:
                return "s " + str(self.table[state_nr].goto.get(symbol))
            return "err"
        else:
            return self.table[state_nr].action

    def save(self, file_name):
        with open(file_name, "w") as f:
            f.write(str(len(self.productions)) + "\n")
            for prod in self.productions:
                f.write(prod.save() + "\n")
            f.write(str(len(self.table)) + "\n")
            for table_elem in self.table:
                f.write(table_elem.save() + "\n")

    @staticmethod
    def load(file_name):
        lr0Table = LR0Table("")
        with open(file_name, "r") as f:
            nr_prod = int(f.readline().strip())
            for i in range(nr_prod):
                lr0Table.productions.append(Production.load(f.readline().strip()))
            nr_table_elem = int(f.readline().strip())
            for i in range(nr_table_elem):
                lr0Table.table.append(TableElem.load(f.readline().strip()))
        return lr0Table


# LR0Table("demo.txt").save("table.txt")
t = LR0Table.load("table.txt")
print(t.table)
