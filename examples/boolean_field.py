from finite_state_machine import StateMachine, transition


def account_in_good_standing(self):
    return len(self.account.bills_outstanding) == 0


class EnableFeatureStateMachine(StateMachine):
    """Example state machine around a feature flag field"""

    def __init__(self, account):
        self.account = account
        self.state = account.feature["enabled"]
        super().__init__()

    @transition(source=False, target=True, conditions=[account_in_good_standing])
    def enable_feature(self):
        pass

    @transition(source=True, target=False)
    def disable_feature(self):
        pass
