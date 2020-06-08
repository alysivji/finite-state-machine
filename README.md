# Finite State Machine

[![Build Status](https://github.com/alysivji/finite-state-machine/workflows/build/badge.svg)](https://github.com/alysivji/finite-state-machine/actions?query=workflow%3A%22build%22)
[![License: MIT](https://img.shields.io/badge/License-MIT-red.svg)](https://opensource.org/licenses/MIT)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

Lightweight, decorator-based Python implementation of a [Finite State Machine](https://en.wikipedia.org/wiki/Finite-state_machine).

## Installation

```console
pip install [name]
```

## Usage

You will need to subclass `StateMachine` and set the `state` instance variable.

The `transition` decorator can be used to specify valid transitions.

## Example

```python
from finite_state_machine import StateMachine, transition

class Turnstile(StateMachine):
    initial_state = "close"

    def __init__(self):
        self.state = self.initial_state

    @transition(source=["close", "open"], target="open")
    def insert_coin(self):
        pass

    @transition(source="open", target="close")
    def pass_thru(self):
        pass
```

### REPL

```console
In [2]: turnstile = Turnstile()

In [3]: turnstile.state
Out[3]: 'close'

In [4]: turnstile.insert_coin()

In [5]: turnstile.state
Out[5]: 'open'

In [6]: turnstile.insert_coin()

In [7]: turnstile.state
Out[7]: 'open'

In [8]: turnstile.pass_thru()

In [9]: turnstile.state
Out[9]: 'close'

In [10]: turnstile.pass_thru()
---------------------------------------------------------------------------
InvalidStartState                         Traceback (most recent call last)
<ipython-input-10-6abc6f4be1cd> in <module>
----> 1 turnstile.pass_thru()

~/state_machine.py in _wrapper(*args, **kwargs)
     32
     33             if self.state not in source:
---> 34                 raise InvalidStartState
     35
     36             for condition in conditions:

InvalidStartState:
```

## Inspiration

This project is inspired by [django-fsm](https://github.com/viewflow/django-fsm/). Wanted a decorator-based state machine without having to use Django.
