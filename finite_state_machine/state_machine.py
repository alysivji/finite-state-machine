import functools
from typing import NamedTuple, Union

from .exceptions import ConditionNotMet, InvalidStartState


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
        raise ValueError("Conditions needs to be a list")

    if on_error:
        if type(on_error) not in allowed_types:
            raise ValueError("on_error needs to be a bool, int or string")

    def transition_decorator(func):
        func.__fsm = Transition(func.__name__, source, target, conditions, on_error)

        @functools.wraps(func)
        def _wrapper(*args, **kwargs):
            try:
                self, rest = args
            except ValueError:
                self = args[0]

            if self.state not in source:
                raise InvalidStartState

            for condition in conditions:
                if not condition(self):
                    raise ConditionNotMet(condition)

            try:
                result = func(*args, **kwargs)
                self.state = target
                return result
            except Exception:
                self.state = on_error

        return _wrapper

    return transition_decorator
