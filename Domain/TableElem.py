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
        table_elem = TableElem("", {})
        txt = txt.split("/*/")
        table_elem.action = txt[0]
        if "s" in table_elem.action:
            for keyval in txt[1].split("/;/"):
                keyval = keyval.split("/;;/")
                table_elem.goto[keyval[0]] = int(keyval[1])
        return table_elem
