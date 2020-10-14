class TransitionNotAllowed(Exception):
    pass


class InvalidStartState(TransitionNotAllowed):
    pass


class ConditionsNotMet(TransitionNotAllowed):
    def __init__(self, conditions):
        conditions_not_met = ", ".join(condition.__name__ for condition in conditions)
        message = f"Following conditions did not return True: {conditions_not_met}"
        super().__init__(message)
