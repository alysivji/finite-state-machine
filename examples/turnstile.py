from finite_state_machine import StateMachine, transition


class Turnstile(StateMachine):
    initial_state = "close"

    def __init__(self):
        self.state = self.initial_state
        super().__init__()

    @transition(source=["close", "open"], target="open")
    def insert_coin(self):
        pass

    @transition(source="open", target="close")
    def pass_thru(self):
        pass
