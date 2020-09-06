# Finite State Machine

[![Build Status](https://github.com/alysivji/finite-state-machine/workflows/build/badge.svg)](https://github.com/alysivji/finite-state-machine/actions?query=workflow%3A%22build%22)
[![License: MIT](https://img.shields.io/badge/License-MIT-red.svg)](https://opensource.org/licenses/MIT)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

Lightweight, decorator-based Python implementation of a [Finite State Machine](https://en.wikipedia.org/wiki/Finite-state_machine).

## Installation

```console
pip install finite-state-machine
```

## Usage

Subclass `StateMachine` and set the `state` instance variable:

```python
from finite_state_machine import StateMachine, transition

class LightSwitch(StateMachine):
    def __init__(self):
        self.state = "off"
        super().__init__()
```

The `transition` decorator can be used to specify valid state transitions
with an optional parameter for `conditions`.
All condition functions need to return `True` for the transition to occur,
else a `ConditionNotMet` exception will be raised.

```python
    @transition(source="off", target="on", conditions=[light_is_off])
    def turn_on(self):
        # specify side effects

def light_is_off(machine):
    return machine.state == "off"
```

Can also specify an `on_error` parameter to handle situations
where the transition function raises an exception:

```python
    @transition(source="off", target="on", on_error="failed")
    def turn_on(self):
        raise ValueError
```

## Example

```python
from finite_state_machine import StateMachine, transition

class Turnstile(StateMachine):
    initial_state = "close"

    def __init__(self):
        self.state = self.initial_state
        super().__init__()

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

The [examples](/examples) folder has additional State Machine workflows.

## Contributing

1. Clone repo
1. Create a virtual environment
1. `pip install -r requirements_dev.txt`
1. Install [pre-commit](https://pre-commit.com/)
1. Set up pre-commit hooks in repo: `pre-commit install`

### Running Tests

```console
pytest
```

## Release

Use SemVer for versioning strategy

### Instructions

1. Grab last version, `X.Y.Z`
1. Generate changelog: `python scripts/generate_changelog.py -v X.Y.Z`
1. Cut a release on GitHub
1. Upload to PyPI with [flit](https://github.com/takluyver/flit)

### Flit Workflow

```console
pip install flit
flit build --format sdist
flit publish --repository testpypi
```

## Inspiration

This project is inspired by [django-fsm](https://github.com/viewflow/django-fsm/). Wanted a decorator-based state machine without having to use Django.
