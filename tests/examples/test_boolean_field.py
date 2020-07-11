from types import SimpleNamespace

import pytest

from finite_state_machine.exceptions import ConditionNotMet, InvalidStartState
from examples.boolean_field import EnableFeatureStateMachine


@pytest.fixture
def create_account():
    def _account(enabled, bills_oustanding=None):
        if bills_oustanding is None:
            bills_oustanding = []
        data = {"feature": {"enabled": enabled}, "bills_outstanding": bills_oustanding}
        return SimpleNamespace(**data)

    return _account


@pytest.mark.parametrize("enabled_state", (True, False))
def test_initilaize_state_machine(create_account, enabled_state):
    account = create_account(enabled=True)
    t = EnableFeatureStateMachine(account)
    assert t.state is True


def test_enabled_account_can_be_disabled(create_account):
    account = create_account(enabled=True)
    t = EnableFeatureStateMachine(account)

    t.disable_feature()
    assert t.state is False


def test_disabled_account_with_no_outstanding_bills_can_be_enabled(create_account):
    account = create_account(enabled=False, bills_oustanding=[])
    t = EnableFeatureStateMachine(account)

    t.enable_feature()
    assert t.state is True


def test_disabled_account_with_oustanding_bill_cannot_be_enabled(create_account):
    account = create_account(enabled=False, bills_oustanding=[1, 2, 3])
    t = EnableFeatureStateMachine(account)

    with pytest.raises(ConditionNotMet):
        t.enable_feature()


def test_enabled_account_cannot_be_reenabled(create_account):
    account = create_account(enabled=True)
    t = EnableFeatureStateMachine(account)

    with pytest.raises(InvalidStartState):
        t.enable_feature()
