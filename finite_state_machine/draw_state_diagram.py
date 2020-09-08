import argparse
import importlib
import inspect
from typing import List

from finite_state_machine.state_machine import Transition


def import_state_machine_class(class_path):
    modname, qualname_separator, qualname = class_path.partition(":")
    obj = importlib.import_module(modname)
    if qualname_separator:
        for attr in qualname.split("."):
            obj = getattr(obj, attr)
    return obj


def create_state_diagram_in_mermaid_markdown(cls):
    class_fns = inspect.getmembers(cls, predicate=inspect.isfunction)
    state_transitions: List[Transition] = [
        func.__fsm for name, func in class_fns if hasattr(func, "__fsm")
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
        mermaid_markdown += f"    [*] --> {cls.initial_state}\n"
        for t in all_state_transitions:
            mermaid_markdown += t

    return mermaid_markdown


def parse_args():
    # TODO make this callable from the command line where you can pass in information
    description = "Create State Diagram for a State Machine"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        "-c",
        "--class",
        type=str,
        help="Path to State Machine class, e.g. importable.module:class",
        required=True,
    )
    return vars(parser.parse_args())


def main():
    args = parse_args()
    class_path = args["class"]
    class_obj = import_state_machine_class(class_path)
    markdown = create_state_diagram_in_mermaid_markdown(class_obj)
    print(markdown)


if __name__ == "__main__":
    main()
