class Node:
    def __init__(self, symbol, index):
        self.symbol = symbol
        self.index = index
        self.parent = None
        self.sibling = None
        self.firstChild = None


class ParserOutput:
    def __init__(self):
        self.root = None
        self.current_node = None

    def recreate_tree(self, outputStack, productions):
        new_node = Node(productions[-1].lhs, 0)
        self.root = new_node
        new_node = Node(productions[-1].rhs[0], 1)
        new_node.parent = self.root
        self.root.firstChild = new_node

        self.add_children(0, outputStack, productions, self.root.firstChild, 2)

    def add_children(self, idx, outputStack, productions, node, nodeIndex):
        siblings = []
        for i in productions[idx].rhs:
            new_node = Node(i, nodeIndex)
            nodeIndex += 1
            new_node.parent = node
            siblings.append(new_node)

        for i in range(len(siblings) - 1):
            siblings[i].sibling = siblings[i + 1]

        node.firstChild = siblings[0]

        idx += 1
        if idx >= len(outputStack) - 1:
            return

        next_node = None
        for i in siblings:
            if i.symbol == productions[outputStack[idx + 1]].lhs:
                next_node = i
                break

        self.add_children(idx, outputStack, productions, next_node, nodeIndex)

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
        table = ""
        table_rows = []

        def traverse_and_print(node, depth):
            if node is not None:
                table_rows.append([
                    depth,
                    node.symbol,
                    node.index,
                    node.parent.index if node.parent else None,
                    node.sibling.index if node.sibling else None
                ])

                child = node.firstChild
                while child:
                    traverse_and_print(child, depth + 1)
                    child = child.sibling

        traverse_and_print(self.root, 0)

        headers = ["Depth", "Symbol", "Index", "Parent", "Right Sibling"]
        table += "\t".join("{:^10}".format(header) for header in headers) + "\n"

        for row in table_rows:
            table += "\t".join("{:^10}".format(str(col)) for col in row) + "\n"

        return table

