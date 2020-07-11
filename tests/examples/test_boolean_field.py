from types import SimpleNamespace

import pytest

from examples.boolean_field import EnableFeatureStateMachine


@pytest.fixture
def account():
    def _account(enabled, bills_oustanding=None):
        if bills_oustanding is None:
            bills_oustanding = []
        data = {"feature": {"enabled": enabled}, "bills_outstanding": bills_oustanding}
        return SimpleNamespace(**data)

    return _account


@pytest.mark.parametrize("enabled_state", (True, False))
def test_initilaize_state_machine(account, enabled_state):
    my_account = account(enabled=True)
    t = EnableFeatureStateMachine(my_account)
    assert t.state is True


def test_disable_enabled_account(account):
    enabled_account = account(enabled=True)
    t = EnableFeatureStateMachine(enabled_account)

    t.disable_feature()
    assert t.state is False


def test_reenable_enabled_account(account):
    enabled_account = account(enabled=True)
    t = EnableFeatureStateMachine(enabled_account)

    t.enable_feature()
    assert t.state is True
