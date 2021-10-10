import argparse
import importlib
import inspect
import os
import sys
from typing import List

from finite_state_machine.state_machine import TransitionDetails


def import_state_machine_class(path):  # pragma: no cover
    """Load State Machine workflow class

    Copied from https://packaging.python.org/specifications/entry-points/#data-model
    """
    modname, qualname_separator, qualname = path.partition(":")
    obj = importlib.import_module(modname)
    if qualname_separator:
        for attr in qualname.split("."):
            obj = getattr(obj, attr)
    return obj


def generate_state_diagram_markdown(cls, initial_state):
    """Create State Diagram in Mermaid Markdown

    https://mermaid-js.github.io/mermaid/diagrams-and-syntax-and-examples/stateDiagram.html
    """

    class_fns = inspect.getmembers(cls, predicate=inspect.isfunction)
    state_transitions: List[TransitionDetails] = [
        func._fsm for name, func in class_fns if hasattr(func, "_fsm")
    ]

    transition_template = "    {source} --> {target} : {name}\n"

    all_state_transitions = []
    for state_transition in state_transitions:
        if isinstance(state_transition.source, list):
            for src in state_transition.source:
                t = transition_template.format(
                    source=src,
                    target=state_transition.target,
                    name=state_transition.name,
                )
                all_state_transitions.append(t)

                if state_transition.on_error:
                    t = transition_template.format(
                        source=src, target=state_transition.on_error, name="on_error"
                    )
                    all_state_transitions.append(t)
        else:
            t = transition_template.format(
                source=state_transition.source,
                target=state_transition.target,
                name=state_transition.name,
            )
            all_state_transitions.append(t)

            if state_transition.on_error:
                t = transition_template.format(
                    source=state_transition.source,
                    target=state_transition.on_error,
                    name="on_error",
                )
                all_state_transitions.append(t)

        mermaid_markdown = "stateDiagram-v2\n"
        if initial_state:
            mermaid_markdown += f"    [*] --> {initial_state}\n"
        for t in all_state_transitions:
            mermaid_markdown += t

    return mermaid_markdown


def parse_args():  # pragma: no cover
    description = "Create State Diagram for a State Machine"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        "--class",
        type=str,
        help="Path to State Machine class, e.g. importable.module:class",
        required=True,
    )
    parser.add_argument(
        "--initial_state",
        type=str,
        help="Initial state of State Machine",
        required=False,
    )
    return vars(parser.parse_args())


def main():  # pragma: no cover
    args = parse_args()
    class_path = args["class"]
    initial_state = args["initial_state"]

    sys.path.append(os.getcwd())
    class_obj = import_state_machine_class(class_path)

    markdown = generate_state_diagram_markdown(class_obj, initial_state)
    print(markdown)


if __name__ == "__main__":
    main()
