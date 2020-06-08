class StateMachine:
    def __init__(self):
        # we save the state here
        pass


def _contains_coin(instance):
    return instance.coin_inserted


def transition(func):
    matrix = {}
    # think we need one more layer

    def _wrapper(self, source, to, conditions=None):
        return func(self, source, to, conditions)
    return _wrapper


class Turnstile:
    STATES = [("open"), ("close")]
    initial_state = "close"

    def __init__(self):
        self.state = self.initial_state
        self.coin_inserted = False

    # @transition(source=["close", "open"], target="open")
    def insert_coin(self):
        self.coin_inserted = True
        self.state = "open"

    # @transition(source="open", target="close", conditions=[_contains_coin])
    def pass_thru(self):
        self.coin_inserted = False
        self.state = "close"
