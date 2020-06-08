class TransitionNotAllowed(Exception):
    pass


class InvalidStartState(TransitionNotAllowed):
    pass


class ConditionNotMet(TransitionNotAllowed):
    def __init__(self, condition):
        self.condition = condition
