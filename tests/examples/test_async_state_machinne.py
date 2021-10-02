import warnings

import pytest

from finite_state_machine.exceptions import InvalidStartState
from examples.async_turnstile import Turnstile


@pytest.mark.asyncio
async def test_async_turnstile_does_not_raise_coroutine_not_awaited_warnings():
    with warnings.catch_warnings(record=True) as caught_warnings:
        t = Turnstile()
        assert t.state == "close"

        result = await t.insert_coin()
        assert t.state == "open"
        assert result == "inserted coin"

        result = await t.insert_coin()
        assert t.state == "open"
        assert result == "inserted coin"

        result = await t.pass_thru()
        assert t.state == "close"
        assert result == "passed thru"

    assert len(caught_warnings) == 0


@pytest.mark.asyncio
async def test_async_turnstile__cannot_pass_thru_closed_turnstile():
    t = Turnstile()
    assert t.state == "close"

    with pytest.raises(
        InvalidStartState, match="Current state is close"
    ), warnings.catch_warnings(record=True) as caught_warnings:
        await t.pass_thru()

    assert len(caught_warnings) == 0
