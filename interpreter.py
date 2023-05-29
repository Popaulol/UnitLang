from __future__ import annotations

import dataclasses
import math
from collections import ChainMap
from pprint import pprint
from typing import Any

from tatsu.walkers import NodeWalker

import unit_type


@dataclasses.dataclass(frozen=True)
class RENDER:
    path: str


def flatten(lst):
    elements = []
    for elm in lst:
        if isinstance(elm, list) or isinstance(elm, tuple):
            elements += flatten(elm)
        else:
            elements.append(elm)
    return elements


def assure_iterable(s):
    if hasattr(s, "__iter__"):
        return s
    else:
        return (s,)


@dataclasses.dataclass
class Function:
    name: str
    parameters: list[str]
    expression: Any
    builtin: bool = False


def sqrt(x):
    return x**0.5


def log(x, base=math.e):
    assert x.unit == unit_type.Unit()
    return unit_type.UnitType(math.log(x.value, base))


def sin(x):
    assert x.unit == unit_type.Unit()
    return unit_type.UnitType(math.sin(x.value))


def cos(x):
    assert x.unit == unit_type.Unit()
    return unit_type.UnitType(math.cos(x.value))


def tan(x):
    assert x.unit == unit_type.Unit()
    return unit_type.UnitType(math.tan(x.value))


class Interpreter(NodeWalker):
    def __init__(self):
        super().__init__()
        self.variables = ChainMap()
        self.functions = {
            "sqrt": Function("sqrt", ["x"], sqrt, True),
            "sin": Function("sin", ["x"], sin, True),
            "cos": Function("cos", ["x"], cos, True),
            "tan": Function("tan", ["x"], tan, True),
            "log": Function("log", ["x", "base"], log, True),
            "ln": Function("log", ["x"], log, True),
        }

    def walk_object(self, node):
        # print(f"object \t\t\t{type(node)=} \t \t {node=}")
        return node

    def walk__number(self, node):
        # print(f"number \t\t\t{type(node)=} \t \t {node=}")
        if node.ast == "":
            return 1.0
        return unit_type.UnitType(float(node.ast))

    def walk__add(self, node):
        # print(f"add \t\t\t{type(node)=} \t \t {node=}")
        return self.walk(node.left) + self.walk(node.right)

    def walk__subtract(self, node):
        # print(f"subtract \t\t{type(node)=} \t \t {node=}")
        return self.walk(node.left) - self.walk(node.right)

    def walk__multiply(self, node):
        # print(f"multiply \t\t{type(node)=} \t \t {node=}")
        return self.walk(node.left) * self.walk(node.right)

    def walk__divide(self, node):
        # print(f"divide \t\t\t{type(node)=} \t \t {node=}")
        return self.walk(node.left) / self.walk(node.right)

    def walk__exponentiate(self, node):
        # print(f"exponentiate \t{type(node)=} \t \t {node=}")
        return self.walk(node.base) ** self.walk(node.exponent)

    def walk__invert(self, node):
        # print(f"invert \t\t\t{type(node)=} \t \t {node=}")
        node = self.walk(node.value)
        # print(f"inverted \t\t\t{type(node)=} \t \t {node=}")
        return -node

    def walk__unit(self, node):
        # print(f"unit \t\t\t{type(node)=} \t \t {node=}")
        unit = ""
        for sub_unit, value in node.ast:
            value = self.walk(value)
            sub_unit = "".join(sub_unit)
            unit = unit + sub_unit + str(value)
        return unit_type.Unit.from_string(unit)

    def walk__unit_number(self, node):
        # print(f"unit_number \t{type(node)=} \t \t {node=}")
        return self.walk(node.value) * self.walk(node.unit)

    def walk__command(self, node):
        match node.cmd:
            case "exit" | "quit":
                exit()
            case "render":
                return RENDER(node.path)
            case "evaluate":
                return self.walk(node.expression)
            case "exclude":
                return self.walk(node.expression)
            case "newline":
                return None
        assert False

    def walk__absolute(self, node):
        return abs(self.walk(node.expr))

    def walk__call(self, node):
        function = self.functions[self.walk(node.function)]
        if function.builtin:
            return function.expression(*assure_iterable(self.walk(node.args)))

        arguments = {}
        for param, arg in zip(
            function.parameters, assure_iterable(self.walk(node.args))
        ):
            arguments[param] = arg

        self.variables = self.variables.new_child(arguments)
        # print(function.expression)
        ret = self.walk(function.expression)
        self.variables = self.variables.parents
        # print(function.expression)
        # print("asdffdgjlkfdgswkljhölkbdsfjkljdfglkjöfgsdkjsgdfljködfgslkjö:" + str(ret))
        return ret

    def walk__access(self, node):
        return self.variables[self.walk(node.name)]

    def walk__variable_definition(self, node):
        self.variables[self.walk(node.name)] = self.walk(node.expression)
        return None

    def walk__function_definition(self, node):
        name = self.walk(node.name)
        args = self.walk(node.args)
        self.functions[name] = Function(name, args, node.expression)
        return None

    def walk__ident(self, node):
        pprint(node)
        return self.walk(node.first) + "".join(node.rest)

    def walk__definition_argument_list(self, node):
        return list(
            filter(
                lambda s: s != ",",
                flatten((self.walk(node.first), self.walk(node.rest))),
            )
        )

    def walk__subexpression(self, node):
        return self.walk(node.expr)
