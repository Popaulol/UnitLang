from pprint import pprint

from tatsu.walkers import NodeWalker

import unit_type


def flatten(lst):
    elements = []
    for elm in lst:
        if isinstance(elm, list) or isinstance(elm, tuple):
            elements += flatten(elm)
        else:
            elements.append(elm)
    return elements


class Renderer(NodeWalker):
    def __init__(self):
        super().__init__()

    def walk_object(self, node):
        return node

    def walk__number(self, node):
        if node.ast == "":
            return "1"
        return node.ast

    def walk__add(self, node):
        return f"{self.walk(node.left)} + {self.walk(node.right)}"

    def walk__subtract(self, node):
        return f"{self.walk(node.left)} - {self.walk(node.right)}"

    def walk__multiply(self, node):
        return rf"{self.walk(node.left)} \cdot {self.walk(node.right)}"

    def walk__divide(self, node):
        return rf"\frac{{ {self.walk(node.left)} }} {{ {self.walk(node.right)} }}"

    def walk__exponentiate(self, node):
        return rf"{{ {self.walk(node.base)} }}^{{ {self.walk(node.exponent)} }}"

    def walk__invert(self, node):
        return rf"-{self.walk(node.value)}"

    def walk__unit(self, node):
        unit = ""
        for sub_unit, value in node.ast:
            value = self.walk(value)
            sub_unit = "".join(sub_unit)
            unit = unit + sub_unit + str(value)
        return unit_type.Unit.from_string(unit).to_latex()

    def walk__unit_number(self, node):
        return f"{self.walk(node.value)} {self.walk(node.unit)}"

    def walk__command(self, node):
        match node.cmd:
            case "exit" | "quit":
                exit()
            case "render":
                return None
            case "evaluate":
                return self.walk(node.expression)
            case "exclude":
                return None
            case "newline":
                return r"\\"
        assert False

    def walk__absolute(self, node):
        return rf"|{self.walk(node.expr)}|"

    def walk__call(self, node):
        args = self.walk(node.args)
        if not isinstance(args, list):
            args = [args]
        return f"{self.walk(node.function)}({', '.join(args)})"

    def walk__access(self, node):
        return self.walk(node.name)

    def walk__variable_definition(self, node):
        return rf"{self.walk(node.name)} &=& {self.walk(node.expression)}"

    def walk__function_definition(self, node):
        return rf"{self.walk(node.name)}({self.walk(node.args)}) &=& {self.walk(node.expression)}"

    def walk__ident(self, node):
        pprint(node)
        return self.walk(node.first) + "".join(node.rest)

    def walk__definition_argument_list(self, node):
        return ", ".join(
            filter(
                lambda s: s != ",",
                flatten((self.walk(node.first), self.walk(node.rest))),
            )
        )

    def walk__subexpression(self, node):
        return f"({self.walk(node.expr)})"
