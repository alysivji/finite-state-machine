import functools


class InvalidStartState(Exception):
    pass


class ConditionNotMet(Exception):
    def __init__(self, condition):
        self.condition = condition


class StateMachine:
    def __init__(self):
        pass


def _contains_coin(instance):
    return instance.coin_inserted


def transition(source, target, conditions=None):
    if isinstance(source, str):
        source = [source]
    if not isinstance(source, list):
        raise ValueError("Source can be a string or list")
    if not isinstance(target, str):
        raise ValueError("Target needs to be a string")
    if not conditions:
        conditions = []
    if not isinstance(conditions, list):
        raise ValueError("Conditions needs to be a list")

    def transition_decorator(func):
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

            result = func(*args, **kwargs)
            self.state = target
            return result

        return _wrapper

    return transition_decorator


class Turnstile:
    STATES = [("open"), ("close")]
    initial_state = "close"

    def __init__(self):
        self.state = self.initial_state
        self.coin_inserted = False

    @transition(source=["close", "open"], target="open")
    def insert_coin(self):
        self.coin_inserted = True
        self.state = "open"

    @transition(source="open", target="close", conditions=[_contains_coin])
    def pass_thru(self):
        self.coin_inserted = False
        self.state = "close"
