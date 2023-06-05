"""
Test for functions that have no type annotations, or type annotations that are
not Pydantic models.

SPDX-FileCopyrightText: 2023-present Waylon S. Walker <waylon@waylonwalker.com>

SPDX-License-Identifier: MIT
"""
import inspect

from engorgio import engorgio


def test_no_pydantic_arg_none() -> None:
    @engorgio()
    def get_alpha(alpha) -> None:
        """Mydocstring."""

    sig = inspect.signature(get_alpha)
    params = sig.parameters
    assert "alpha" in params
    param = params["alpha"]
    assert param.annotation is inspect.Parameter.empty
    assert param.default == str(inspect.Parameter.empty)


def test_no_pydantic_kwarg_none() -> None:
    @engorgio()
    def get_alpha(alpha=None) -> None:
        """Mydocstring."""

    sig = inspect.signature(get_alpha)
    params = sig.parameters
    assert "alpha" in params
    param = params["alpha"]
    assert param.annotation is inspect.Parameter.empty
    assert param.default == "None"


def test_no_pydantic_arg_str_none() -> None:
    @engorgio()
    def get_alpha(alpha: str) -> None:
        """Mydocstring."""

    sig = inspect.signature(get_alpha)
    params = sig.parameters
    assert "alpha" in params
    param = params["alpha"]
    assert param.annotation == str
    assert param.default == str(inspect.Parameter.empty)


def test_no_pydantic_kwarg_str_none() -> None:
    @engorgio()
    def get_alpha(alpha: str = None) -> None:
        """Mydocstring."""

    sig = inspect.signature(get_alpha)
    params = sig.parameters
    assert "alpha" in params
    param = params["alpha"]
    assert param.annotation == str
    assert param.default == "None"


def test_no_pydantic_kwarg_str_default() -> None:
    @engorgio()
    def get_alpha(alpha: str = "hello") -> None:
        """Mydocstring."""

    sig = inspect.signature(get_alpha)
    params = sig.parameters
    assert "alpha" in params
    param = params["alpha"]
    assert param.annotation == str
    assert param.default == "hello"
