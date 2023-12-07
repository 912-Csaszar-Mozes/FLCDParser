from functools import partial

from Domain.LR0Table import LR0Table


class Menu:
    def __init__(self, input_file, output_file):
        """
        I wanted to try something different with this menu.
        In order to add a menu command you need to use "lambda:" otherwise the functions inside self.menu_commands will
        be executed when the class is initialized.
        You also need to use partial(function)(arguments) in order to avoid functions being executed early.
        :param input_file:
        :param output_file:
        """
        self.lr0Table = LR0Table(input_file)  # TODO This might have to be changed with Grammar class in the future
        self.lr0Table.save(output_file)
        self.table = LR0Table.load(output_file)

        self.menu_commands = {
            "0": exit,
            "1": lambda: print("The terminals are as follows: " + str(self.lr0Table.terminals)),
            "2": lambda: print("The non-terminals are as follows: " + str(self.lr0Table.non_terminals)),
            "3": lambda: print("The productions are as follows: " + str(self.lr0Table.productions)),
            "4": lambda: partial(self.print_productions)(input("Input your production: ")),
            "5": lambda: print("The productions are as follows: " + str(self.table.table)),
            "6": lambda: print("The given grammar is context-free"
                               if partial(self.check_cfg)() else "The given grammar is NOT context-free"),
        }

    @staticmethod
    def display_commands():
        """
        Prints the commands to the command line.
        """
        print("\n\t0. Exit\n"
              "\t1. Show terminals\n"
              "\t2. Show non-terminals\n"
              "\t3. Show productions\n"
              "\t4. Show productions for a given non_terminal\n"
              "\t5. Show LR0 Table\n"
              "\t6. Check CFG\n")

    def check_cfg(self):
        """
        Checks if the grammar is a context-free grammar by making sure each production has only one non-terminal
        :return: True if the grammar is context-free, False otherwise
        """
        for production in self.lr0Table.productions:
            if " " in production.lhs or production.lhs not in self.lr0Table.non_terminals:
                return False
        return True

    def print_productions(self, non_terminal):
        """
        Prints all productions for a given non-terminal
        :param non_terminal: The given non-terminal
        :return: All productions associated to the non-terminal that was provided
        """
        if non_terminal not in self.lr0Table.non_terminals:
            print("The given non-terminal does not have any productions associated with it!")
        else:
            print(f"The productions for the non-terminal \"{non_terminal}\" are as follows: ")
            for production in self.lr0Table.productions:
                if production.lhs == non_terminal:
                    print(production)

    def run(self):
        """
        Starts the execution of the menu
        """
        while True:
            self.display_commands()

            option = input("Choose an option: ")
            if option in self.menu_commands:
                self.menu_commands[option]()
            else:
                print("Wrong input was given!")


menu = Menu("g1.txt", "table.txt")
menu.run()
