from enum import Enum
import functools
import types
from typing import NamedTuple, Union

from .exceptions import ConditionsNotMet, InvalidStartState


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
    allowed_types = (str, bool, int, Enum)

    if isinstance(source, allowed_types):
        source = [source]
    if not isinstance(source, list):
        raise ValueError("Source can be a bool, int, string, Enum, or list")
    for item in source:
        if not isinstance(item, allowed_types):
            raise ValueError("Source can be a bool, int, string, Enum, or list")

    if not isinstance(target, allowed_types):
        raise ValueError("Target needs to be a bool, int or string")

    if not conditions:
        conditions = []
    if not isinstance(conditions, list):
        raise ValueError("conditions must be a list")
    for condition in conditions:
        if not isinstance(condition, types.FunctionType):
            raise ValueError("conditions list must contain functions")

    if on_error:
        if not isinstance(on_error, allowed_types):
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
                exception_message = (
                    f"Current state is {self.state}. "
                    f"{func.__name__} allows transitions from {source}."
                )
                raise InvalidStartState(exception_message)

            conditions_not_met = []
            for condition in conditions:
                if not condition(*args, **kwargs):
                    conditions_not_met.append(condition)
            if conditions_not_met:
                raise ConditionsNotMet(conditions_not_met)

            if not on_error:
                result = func(*args, **kwargs)
                self.state = target
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
