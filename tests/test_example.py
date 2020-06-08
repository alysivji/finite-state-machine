import pytest
from finite_state_machine.example import Turnstile, InvalidStartState


def test_turnstile():
    t = Turnstile()
    assert t.state == "close"
    assert not t.coin_inserted

    t.insert_coin()
    assert t.state == "open"
    assert t.coin_inserted

    t.insert_coin()
    assert t.state == "open"
    assert t.coin_inserted

    t.pass_thru()
    assert t.state == "close"
    assert not t.coin_inserted


def test_turnstile__cannot_pass_thru_closed_turnstile():
    t = Turnstile()
    assert t.state == "close"
    assert not t.coin_inserted

    with pytest.raises(InvalidStartState):
        t.pass_thru()
