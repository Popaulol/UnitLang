from __future__ import annotations

import copy
import dataclasses
import json
from pprint import pprint
from typing import Any

import tatsu
from tatsu.util import asjson

import LaTeX_renderer
import unit_type
from interpreter import RENDER, Interpreter

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
        to_be_saved = copy.deepcopy(model)
        result = interpreter.walk(model)
        run_commands.append(Line(to_be_saved, result))
        pprint(run_commands)
        if isinstance(result, RENDER):
            latex_render = LaTeX_renderer.Renderer()
            with open(result.path, "w") as f:
                f.write("\\begin{align}\n")
                for line in run_commands:
                    latex = latex_render.walk(line.model)
                    if latex is not None:
                        f.write(latex)
                        if line.result is not None and not isinstance(
                            line.result, RENDER
                        ):
                            f.write(" &=& ")
                            f.write(line.result.to_latex())
                        f.write("\\\\\n")
                f.write(r"\end{align}")
        elif result is not None:
            print(result)


if __name__ == "__main__":
    main()
