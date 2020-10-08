import functools
import types
from typing import NamedTuple, Union

from .exceptions import ConditionsNotMet, InvalidStartState, TransitionNotAllowed


class StateMachine:
    def __init__(self):
        try:
            self.state
        except AttributeError:
            raise ValueError("Need to set a state instance variable")


class Transition(NamedTuple):
    name: str
    source: Union[list, bool, int, str]
    target: Union[bool, int, str]
    conditions: list
    on_error: Union[bool, int, str]


class TransitionMeta(object):
    def __init__(self, name):
        self.name = name
        self.transitions = {}

    def get_transition(self, source):
        transition = self.transitions.get(source, None)
        if transition is None:
            transition = self.transitions.get("*", None)
        if transition is None:
            transition = self.transitions.get("+", None)
        return transition

    def add_transition(self, source, target, on_error=None, conditions=[]):
        if source in self.transitions:
            raise AssertionError("Duplicate transition for {0} state".format(source))
        self.transitions[source] = Transition(
            name=self.name, source=source, target=target, on_error=on_error, conditions=conditions
        )

    def next_state(self, current_state):
        transition = self.get_transition(current_state)
        if transition is None:
            raise TransitionNotAllowed("No transition from {0}".format(current_state))
        return transition.target


def transition(source, target, conditions=None, on_error=None):
    allowed_types = [str, bool, int]

    if type(source) in allowed_types:
        source = [source]
    if not isinstance(source, list):
        raise ValueError("Source can be a bool, int, string or list")

    if type(target) not in allowed_types:
        raise ValueError("Target needs to be a bool, int or string")

    if not conditions:
        conditions = []
    if not isinstance(conditions, list):
        raise ValueError("conditions must be a list")
    for condition in conditions:
        if not isinstance(condition, types.FunctionType):
            raise ValueError("conditions list must contain functions")

    if on_error:
        if type(on_error) not in allowed_types:
            raise ValueError("on_error needs to be a bool, int or string")

    def transition_decorator(func):
        func.__fsm = TransitionMeta(func.__name__)
        if isinstance(source, (list, tuple, set)):
            for item in source:
                func.__fsm.add_transition(item, target, on_error, conditions)
        else:
            func.__fsm.add_transition(source, target, on_error, conditions)

        @functools.wraps(func)
        def _wrapper(*args, **kwargs):
            try:
                self, rest = args
            except ValueError:
                self = args[0]

            if self.state not in func.__fsm.transitions:
                exception_message = (
                    f"Current state is {self.state}. "
                    f"{func.__fsm.name} allows transitions from {func.__fsm.transitions}."
                )
                raise InvalidStartState(exception_message)

            conditions_not_met = []
            for condition in func.__fsm.transitions[self.state].conditions:
                if not condition(*args, **kwargs):
                    conditions_not_met.append(condition)
            if conditions_not_met:
                raise ConditionsNotMet(conditions_not_met)

            if not on_error:
                result = func(*args, **kwargs)
                self.state = func.__fsm.transitions[self.state].target
                return result

            try:
                result = func(*args, **kwargs)
                self.state = target
                return result
            except Exception:
                # TODO should we log this somewhere?
                # logger.error? maybe have an optional parameter to set this up
                # how to libraries log?
                self.state = on_error
                return

        return _wrapper

    return transition_decorator
