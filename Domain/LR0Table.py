from Domain.Grammar import Grammar
from Domain.Item import Item
from Domain.Production import Production
from Domain.State import State
from Domain.TableElem import TableElem


class LR0Table:
    def closure(self, state):
        changed = True
        while changed:
            changed = False
            for item in state.items:
                symbol_after_dot = item.symbol_after_dot()
                if symbol_after_dot in self.grammar.non_terminals:
                    for prod in self.grammar.productions:
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
        self.grammar = Grammar(file_name)
        self.states = []
        self.table = []
        if file_name != "":
            gotos = self.canonical_collection()
            self.create(gotos)

    def state_pos(self, state):
        for i in range(len(self.states)):
            if self.states[i] == state:
                return i
        return -1

    def get_goto(self, state_nr, symbol):
        return self.table[state_nr].goto.get(symbol)

    # calculate states and closure
    def canonical_collection(self):
        gotos = {}
        self.states.append(self.closure(State(0, [Item(self.grammar.productions[0], 0)])))
        i = 0
        while i < len(self.states):
            state = self.states[i]
            for s in self.grammar.symbols:
                new_state = self.goto(state, s)
                if len(new_state.items) != 0:
                    state_pos = self.state_pos(new_state)
                    new_state.nr = len(self.states) if state_pos == -1 else state_pos
                    if state_pos == -1:
                        self.states.append(new_state)
                    # add calculated state to goto list
                    if gotos.get(i) is not None:
                        gotos[i].append((s, new_state.nr))
                    else:
                        gotos[i] = [(s, new_state.nr)]
            i += 1
        return gotos

    # fill in the table
    def create(self, gotos):
        for i in range(len(self.states)):
            # see if it is reduce or accept
            action = ""
            state = self.states[i]
            table_elem = TableElem("", {})
            # add reduce items
            for item in state.items:
                if item.symbol_after_dot() is None:
                    if action == "":
                        if item.prod == self.grammar.productions[0]:
                            action = "a"
                        else:
                            action = "r " + str(item.prod.nr)
                    else:
                        raise Exception("REDUCE-REDUCE CONFLICT with state \n `{}` \n at symbol `{}`".format(state, item))
            # add shift items
            for goto in gotos.get(i, []):
                if action == "" or action == "s":
                    table_elem.goto[goto[0]] = goto[1]
                    action = "s"
                else:
                    raise Exception("SHIFT-REDUCE CONFLICT with state \n `{}` \n at symbol `{}`".format(state, goto[0]))
            table_elem.action = action
            self.table.append(table_elem)

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
        with open("OutputFiles/" + file_name, "w") as f:
            f.write(self.grammar.save() + "\n")
            f.write(str(len(self.grammar.productions)) + "\n")
            for prod in self.grammar.productions:
                f.write(prod.save() + "\n")
            f.write(str(len(self.table)) + "\n")
            for table_elem in self.table:
                f.write(table_elem.save() + "\n")

    @staticmethod
    def load(file_name):
        lr0Table = LR0Table("")
        with open("OutputFiles/" + file_name, "r") as f:
            lr0Table.grammar.load(f.readline())
            nr_prod = int(f.readline().strip())
            for i in range(nr_prod):
                lr0Table.grammar.productions.append(Production.load(f.readline().strip()))
            nr_table_elem = int(f.readline().strip())
            for i in range(nr_table_elem):
                lr0Table.table.append(TableElem.load(f.readline().strip()))
        return lr0Table
