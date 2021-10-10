from finite_state_machine import StateMachine, transition


class Turnstile(StateMachine):
    initial_state = "close"

    def __init__(self):
        self.state = self.initial_state
        super().__init__()

    @transition(source=["close", "open"], target="open", on_error="error_state")
    async def insert_coin(self):
        return "inserted coin"

    @transition(source="open", target="close")
    async def pass_thru(self):
        return "passed thru"

    @transition(source="close", target="close", on_error="error_state")
    async def error_function(self):
        raise ValueError
