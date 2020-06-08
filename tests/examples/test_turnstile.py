import pytest

from finite_state_machine.exceptions import InvalidStartState
from examples.turnstile import Turnstile


def test_turnstile():
    t = Turnstile()
    assert t.state == "close"

    t.insert_coin()
    assert t.state == "open"

    t.insert_coin()
    assert t.state == "open"

    t.pass_thru()
    assert t.state == "close"


def test_turnstile__cannot_pass_thru_closed_turnstile():
    t = Turnstile()
    assert t.state == "close"

    with pytest.raises(InvalidStartState):
        t.pass_thru()
