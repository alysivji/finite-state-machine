from finite_state_machine import StateMachine
import pytest


def test_state_machine():
    class LightSwitch(StateMachine):
        def turn_on(self):
            pass

        def turn_off(self):
            pass

    with pytest.raises(ValueError):
        LightSwitch()
