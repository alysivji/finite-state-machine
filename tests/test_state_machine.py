from finite_state_machine import StateMachine, transition
import pytest


def test_state_machine_requires_state_instance_variable():
    class LightSwitch(StateMachine):
        def turn_on(self):
            pass

        def turn_off(self):
            pass

    with pytest.raises(ValueError, match="Need to set a state instance variable"):
        LightSwitch()


def test_source_parameter_is_tuple():
    with pytest.raises(ValueError, match="Source can be a"):

        @transition(source=("here",), target="there")
        def conditions_check(instance):
            pass


def test_target_parameter_is_tuple():
    with pytest.raises(ValueError, match="Target needs to be a"):

        @transition(source="here", target=("there",))
        def conditions_check(instance):
            pass


def test_conditions_parameter_is_tuple():
    with pytest.raises(ValueError, match="Conditions needs to be a list"):

        @transition(source="here", target="there", conditions=(1, 2))
        def conditions_check(instance):
            pass


class TestExceptionStateHandling:
    def test_on_error_parameter_is_invalid(self):
        with pytest.raises(ValueError, match="on_error needs to be"):

            @transition(source="here", target="there", on_error=(1, 2))
            def state_transition(instance):
                pass

    def test_state_machine_goes_into_on_error_state_when_exception_occurs(self):
        """happy path when error occurs"""

        class LightSwitch(StateMachine):
            def __init__(self):
                self.state = "off"

            @transition(source="off", target="on", on_error="failed")
            def turn_on(self):
                raise ValueError

            @transition(source="on", target="off")
            def turn_off(self):
                pass

        # Arrange
        switch = LightSwitch()
        assert switch.state == "off"

        # Act
        switch.turn_on()

        # Assert
        assert switch.state == "failed"

    def test_state_machine_transition_function_does_not_raise_exception(self):
        """happy path => when transition function runs without an error"""

        class LightSwitch(StateMachine):
            def __init__(self):
                self.state = "off"

            @transition(source="off", target="on", on_error="failed")
            def turn_on(self):
                pass

            @transition(source="on", target="off", on_error="failed")
            def turn_off(self):
                pass

        # Arrange
        switch = LightSwitch()
        assert switch.state == "off"

        # Act
        switch.turn_on()

        # Assert
        assert switch.state == "on"

    def test_on_error_parameter_is_not_set_and_transition_function_raises_error(self):
        """Transition function raises error, but on_error parameter is not set"""

        class LightSwitch(StateMachine):
            def __init__(self):
                self.state = "off"

            @transition(source="off", target="on")
            def turn_on(self):
                raise ValueError("expected error")

            @transition(source="on", target="off")
            def turn_off(self):
                pass

        # Arrange
        switch = LightSwitch()
        assert switch.state == "off"

        # Act / Assert
        with pytest.raises(ValueError, match="expected error"):
            switch.turn_on()
