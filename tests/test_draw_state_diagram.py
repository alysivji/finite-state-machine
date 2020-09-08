from finite_state_machine import StateMachine, transition
from finite_state_machine.draw_state_diagram import generate_state_diagram_markdown


def test_turnstile_diagram_without_initial_state():
    # Arrange
    class Turnstile(StateMachine):
        initial_state = "close"

        @transition(source=["close", "open"], target="open")
        def insert_coin(self):
            pass

        @transition(source="open", target="close", on_error="failed")
        def pass_thru(self):
            pass

    # Act
    mermaid_markdown = generate_state_diagram_markdown(Turnstile, initial_state=None)

    # Assert
    assert "stateDiagram-v2" in mermaid_markdown
    assert "close --> open : insert_coin" in mermaid_markdown
    assert "open --> open : insert_coin" in mermaid_markdown
    assert "open --> close : pass_thru" in mermaid_markdown
    assert "open --> failed : on_error" in mermaid_markdown


def test_turnstile_diagram_with_initial_state():
    # Arrange
    class Turnstile(StateMachine):
        initial_state = "close"

        @transition(source=["close", "open"], target="open")
        def insert_coin(self):
            pass

        @transition(source="open", target="close", on_error="failed")
        def pass_thru(self):
            pass

    # Act
    mermaid_markdown = generate_state_diagram_markdown(Turnstile, initial_state="close")

    # Assert
    assert "stateDiagram-v2" in mermaid_markdown
    assert "[*] --> close" in mermaid_markdown
    assert "close --> open : insert_coin" in mermaid_markdown
    assert "open --> open : insert_coin" in mermaid_markdown
    assert "open --> close : pass_thru" in mermaid_markdown
    assert "open --> failed : on_error" in mermaid_markdown
