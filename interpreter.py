from tatsu.walkers import NodeWalker

import unit_type


class Interpreter(NodeWalker):
    def walk_object(self, node):
        print(f"object \t\t\t{type(node)=} \t \t {node=}")
        return node

    def walk__number(self, node):
        print(f"number \t\t\t{type(node)=} \t \t {node=}")
        if node.ast == "":
            return 1.0
        return unit_type.UnitType(float(node.ast))

    def walk__add(self, node):
        print(f"add \t\t\t{type(node)=} \t \t {node=}")
        return self.walk(node.left) + self.walk(node.right)

    def walk__subtract(self, node):
        print(f"subtract \t\t{type(node)=} \t \t {node=}")
        return self.walk(node.left) - self.walk(node.right)

    def walk__multiply(self, node):
        print(f"multiply \t\t{type(node)=} \t \t {node=}")
        return self.walk(node.left) * self.walk(node.right)

    def walk__divide(self, node):
        print(f"divide \t\t\t{type(node)=} \t \t {node=}")
        return self.walk(node.left) / self.walk(node.right)

    def walk__exponentiate(self, node):
        print(f"exponentiate \t{type(node)=} \t \t {node=}")
        return self.walk(node.base) ** self.walk(node.exponent)

    def walk__invert(self, node):
        print(f"invert \t\t\t{type(node)=} \t \t {node=}")
        node = self.walk(node.value)
        print(f"inverted \t\t\t{type(node)=} \t \t {node=}")
        return -node

    def walk__unit(self, node):
        print(f"unit \t\t\t{type(node)=} \t \t {node=}")
        unit = ""
        for sub_unit, value in node.ast:
            value = self.walk(value)
            sub_unit = "".join(sub_unit)
            unit = unit + sub_unit + str(value)
        return unit_type.Unit.from_string(unit)

    def walk__unit_number(self, node):
        print(f"unit_number \t{type(node)=} \t \t {node=}")
        return self.walk(node.value) * self.walk(node.unit)

    def walk__command(self, node):
        match node.cmd:
            case 'exit' | 'quit':
                exit()
            case 'render':
                assert False
            case 'evaluate':
                return self.walk(node.expression)
            case 'exclude':
                assert False
        assert False
