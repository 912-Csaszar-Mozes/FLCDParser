class Node:
    def __init__(self, symbol, data=None):
        self.symbol = symbol
        self.data = data
        self.parent = None
        self.sibling = None
        self.firstChild = None


class ParserOutput:
    def __init__(self):
        self.root = None
        self.current_node = None

    def recreate_tree(self, outputStack, productions, non_terminals):
        print(productions)
        new_node = Node(productions[-1].lhs)
        self.root = new_node
        new_node = Node(productions[-1].rhs[0])
        new_node.parent = self.root
        self.root.firstChild = new_node

        self.print_to_screen()

    def add_node(self, symbol, data=None):
        new_node = Node(symbol, data)
        if self.current_node is None:
            self.root = new_node
        else:
            if self.current_node.firstChild is None:
                self.current_node.firstChild = new_node
            else:
                current_child = self.current_node.firstChild
                while current_child.sibling:
                    current_child = current_child.sibling
                current_child.sibling = new_node
            new_node.parent = self.current_node
        self.current_node = new_node

    def ascend_tree(self):
        if self.current_node:
            self.current_node = self.current_node.parent

    def transform_tree(self):
        # Turns the tree into a printable string
        return self._transform_tree_recursive(self.root)

    def _transform_tree_recursive(self, node):
        if node is None:
            return ""
        result = node.symbol
        child = node.firstChild
        while child:
            result += self._transform_tree_recursive(child)
            child = child.sibling
        return result

    def print_to_screen(self):
        print(self._create_table())

    def print_to_file(self, file_path):
        with open(file_path, "w") as file:
            file.write(self._create_table())

    def _create_table(self):
        # Initialize a list to store rows of the table
        table = ""
        table_rows = []

        # Helper function to recursively traverse the tree and populate the table
        def traverse_and_print(node, depth):
            if node is not None:
                # Add a row for the current node
                table_rows.append([
                    depth,
                    node.symbol,
                    node.data,
                    node.parent.symbol if node.parent else None,
                    node.firstChild.symbol if node.firstChild else None
                ])

                # Recursively process the children of the current node
                child = node.firstChild
                while child:
                    traverse_and_print(child, depth + 1)
                    child = child.sibling

        # Start traversing the tree from the root
        traverse_and_print(self.root, 0)

        # Print the table headers with centered content
        headers = ["Depth", "Symbol", "Data", "Parent", "FirstChild"]
        table += "\t".join("{:^10}".format(header) for header in headers) + "\n"

        # Print each row of the table with centered content
        for row in table_rows:
            table += "\t".join("{:^10}".format(str(col)) for col in row) + "\n"

        return table

