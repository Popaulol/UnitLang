from __future__ import annotations

import dataclasses
import json
from pprint import pprint
from typing import Any

import tatsu
from tatsu.util import asjson

import unit_type
from interpreter import Interpreter

# "1m10N100mol2K-3459cd-56V-23 * -(3 + 5 * ( 10 - 100**(-0.5) ))"

GRAMMAR: str | None = None

run_commands = []


@dataclasses.dataclass
class Line:
    model: Any
    result: unit_type.UnitType


def main() -> None:
    global GRAMMAR
    with open("grammar.ebnf") as f:
        GRAMMAR = f.read()

    parser = tatsu.compile(GRAMMAR, asmodel=True)
    interpreter = Interpreter()

    while True:
        model = parser.parse(input(">>> "))
        print(json.dumps(asjson(model), indent=4))
        pprint(model)

        # with open("ast.dot", "w") as f:
        #    f.write("digraph {\n")
        #    f.write(AstRenderer().walk(model))
        #    f.write("}")
        #
        result = interpreter.walk(model)
        if result is not None:
            print(result)
        run_commands.append(Line(model, result))


if __name__ == "__main__":
    main()
