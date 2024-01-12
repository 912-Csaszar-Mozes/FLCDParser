from Domain.ParserOutput import ParserOutput
from Domain.LR0Table import LR0Table


class LR0Parser:
    def __init__(self, lr0_table):
        self.lr0_table = lr0_table
        self.stack = []
        self.output = ParserOutput()
        self.outputStack = []

    def parse(self, input_string):
        self.stack.append(0)

        idx = 0
        print("Beginning parsing. Stack:", self.stack, "Input:", input_string[idx:])
        while True:
            current_state = self.stack[-1]
            current_symbol = input_string[idx] if idx < len(input_string) else None

            print(current_state, current_symbol)
            action = self.lr0_table.get_action(current_state, current_symbol)

            print("START Action:", action, "Stack:", self.stack, "Input:", input_string[idx:])

            if action == 'err':
                print("Error: No action defined for state", current_state, "and symbol", current_symbol)
                break

            if action.startswith('s'):
                new_state = int(action.split()[1])
                self.stack.append(new_state)
                self.output.add_node(current_symbol)  # Add terminal node
                idx += 1  # Move to the next input symbol

            elif action.startswith('r'):
                production_number = int(action.split()[1])
                production = self.lr0_table.grammar.productions[production_number]
                lhs, rhs = production.lhs, production.rhs

                # Pop the stack and ascend the tree in the output
                for _ in range(len(rhs)):
                    self.stack.pop()
                    self.output.ascend_tree()
                print(production)
                self.outputStack.insert(0, production_number)

                self.output.add_node(lhs)  # Add nonterminal node after reduction

                # goto_state = self.lr0_table.get_goto(current_state, lhs)
                # if goto_state is not None:
                #     self.stack.append(goto_state)
                temp_action = self.lr0_table.get_action(self.stack[-1], self.output.current_node.symbol)
                if temp_action.startswith('s'):
                    new_state = int(temp_action.split(" ")[1])
                    self.stack.append(new_state)

            if action == 'a':
                if idx == len(input_string):
                    self.output.add_node("S")
                    self.outputStack.insert(0, 0)
                    self.output.add_node("S'")
                    self.outputStack.insert(0, -1)
                    print("Parsing completed successfully.")
                else:
                    print("Error: Extra input symbols after parsing completion.")
                break

            print("END Action:", action, "Stack:", self.stack, "Input:", input_string[idx:])

        self.output.recreate_tree(self.outputStack, self.lr0_table.grammar.productions, self.lr0_table.grammar.non_terminals)
        return self.output


lr0_table = LR0Table("InputFiles\g1.txt")
print("lr0table: " + str(lr0_table.table))

lr0_parser = LR0Parser(lr0_table)
parser_output = lr0_parser.parse('abc')

# parser_output.print_to_file('OutputFiles\parserOutput.txt')
# lr0_parser.output.print_to_screen()
# print(lr0_parser.output.transform_tree())
# print(lr0_parser.outputStack)
# print(lr0_parser.lr0_table.grammar.productions)