import operator
from functools import reduce

from tatsu.walkers import NodeWalker


class AstRenderer(NodeWalker):
    def walk_object(self, node):
        print("START WALK" + "--------------" * 10)
        graph = (
            reduce(operator.add, (self.walk(n) for n in node._children), "")
            if node._children is not None
            else ""
        )
        label = type(node).__name__ + ":\\n"
        members = [
            attr
            for attr in dir(node)
            if not callable(getattr(node, attr))
            and not attr.startswith("_")
            and not attr == "ast"
        ]
        for member in members:
            if getattr(node, member) is None:
                continue
            print(f"{member} = {getattr(node, member)}")
            label += f"{member} = {getattr(node, member)}, \\n"

        label = label.replace('"', "'")
        label = label.replace("\n", "\\n")
        assert '"' not in label
        assert "\n" not in label
        graph = graph + f'{id(node)} [label="{label}"];\n'
        if node._children is not None:
            for n in node._children:
                graph = graph + f"{id(node)} -> {id(n)};\n"
        print("END WALK" + "--------------" * 10)
        return graph
