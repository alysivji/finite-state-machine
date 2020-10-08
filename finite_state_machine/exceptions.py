class TransitionNotAllowed(Exception):
    pass


class InvalidStartState(TransitionNotAllowed):
    pass


class ConditionsNotMet(TransitionNotAllowed):
    def __init__(self, conditions):
        conditions_not_met = ", ".join(condition.__name__ for condition in conditions)
        message = f"Following conditions did not return True: {conditions_not_met}"
        super().__init__(message)

class TransitionNotAllowed(Exception):
    def __init__(self, *args, **kwargs):
        self.object = kwargs.pop('object', None)
        self.method = kwargs.pop('method', None)
        super(TransitionNotAllowed, self).__init__(*args, **kwargs)