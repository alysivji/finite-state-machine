from .turnstile import Turnstile


class TurnstileWithLog(Turnstile):
    def __init__(self):
        super().__init__()
        self.history = [self.state]

    def on_state_change(self, source, target):
        if source != target:
            self.history.append(target)
