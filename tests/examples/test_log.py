import pytest

from finite_state_machine.exceptions import InvalidStartState
from examples.log import TurnstileWithLog


def test_turnstile():
    t = TurnstileWithLog()
    assert t.state == "close"
    assert t.history == ["close"]

    t.insert_coin()
    assert t.state == "open"
    assert t.history == ["close", "open"]

    t.insert_coin()
    assert t.state == "open"
    assert t.history == ["close", "open"]

    t.pass_thru()
    assert t.state == "close"
    assert t.history == ["close", "open", "close"]


def test_turnstile__cannot_pass_thru_closed_turnstile():
    t = TurnstileWithLog()
    assert t.state == "close"

    with pytest.raises(InvalidStartState, match="Current state is close"):
        t.pass_thru()
