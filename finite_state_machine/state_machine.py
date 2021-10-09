import asyncio
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


class transition:
    _fsm_transition_mapping = {}

    def __init__(self, source, target, conditions=None, on_error=None):
        allowed_types = (str, bool, int, Enum)

        if isinstance(source, allowed_types):
            source = [source]
        if not isinstance(source, list):
            raise ValueError("Source can be a bool, int, string, Enum, or list")
        for item in source:
            if not isinstance(item, allowed_types):
                raise ValueError("Source can be a bool, int, string, Enum, or list")
        self.source = source

        if not isinstance(target, allowed_types):
            raise ValueError("Target needs to be a bool, int or string")
        self.target = target

        if not conditions:
            conditions = []
        if not isinstance(conditions, list):
            raise ValueError("conditions must be a list")
        for condition in conditions:
            if not isinstance(condition, types.FunctionType):
                raise ValueError("conditions list must contain functions")
        self.conditions = conditions

        if on_error:
            if not isinstance(on_error, allowed_types):
                raise ValueError("on_error needs to be a bool, int or string")
        self.on_error = on_error

    def __call__(self, func):
        func.__fsm = Transition(
            func.__name__,
            self.source,
            self.target,
            self.conditions,
            self.on_error,
        )
        # TODO update on class transition mapping
        self.__class__._fsm_transition_mapping[func.__qualname__] = func

        @functools.wraps(func)
        def callable(*args, **kwargs):
            try:
                state_machine, rest = args
            except ValueError:
                state_machine = args[0]

            if state_machine.state not in self.source:
                exception_message = (
                    f"Current state is {state_machine.state}. "
                    f"{func.__name__} allows transitions from {self.source}."
                )
                raise InvalidStartState(exception_message)

            conditions_not_met = []
            for condition in self.conditions:
                if condition(*args, **kwargs) is not True:
                    conditions_not_met.append(condition)
            if conditions_not_met:
                raise ConditionsNotMet(conditions_not_met)

            if not self.on_error:
                result = func(*args, **kwargs)
                state_machine.state = self.target
                return result

            try:
                result = func(*args, **kwargs)
                state_machine.state = self.target
                return result
            except Exception:
                # TODO should we log this somewhere?
                # logger.error? maybe have an optional parameter to set this up
                # how to libraries log?
                state_machine.state = self.on_error
                return

        @functools.wraps(func)
        async def async_callable(*args, **kwargs):
            try:
                state_machine, rest = args
            except ValueError:
                state_machine = args[0]

            if state_machine.state not in self.source:
                exception_message = (
                    f"Current state is {state_machine.state}. "
                    f"{func.__name__} allows transitions from {self.source}."
                )
                raise InvalidStartState(exception_message)

            conditions_not_met = []
            for condition in self.conditions:
                if asyncio.iscoroutinefunction(condition):
                    condition_result = await condition(*args, **kwargs)
                else:
                    condition_result = condition(*args, **kwargs)
                if condition_result is not True:
                    conditions_not_met.append(condition)
            if conditions_not_met:
                raise ConditionsNotMet(conditions_not_met)

            if not self.on_error:
                result = await func(*args, **kwargs)
                state_machine.state = self.target
                return result

            try:
                result = await func(*args, **kwargs)
                state_machine.state = self.target
                return result
            except Exception:
                # TODO should we log this somewhere?
                # logger.error? maybe have an optional parameter to set this up
                # how to libraries log?
                state_machine.state = self.on_error
                return

        if asyncio.iscoroutinefunction(func):
            return async_callable
        else:
            return callable
