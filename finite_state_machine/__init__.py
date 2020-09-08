"""Lightweight, decorator-based implementation of a Finite State Machine"""

__version__ = "0.2.0"


from .draw_state_diagram import create_state_diagram_in_mermaid_markdown  # noqa
from .state_machine import StateMachine, transition  # noqa
