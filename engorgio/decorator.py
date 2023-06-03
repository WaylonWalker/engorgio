"""engorgio.

SPDX-FileCopyrightText: 2023-present Waylon S. Walker <waylon@waylonwalker.com>

SPDX-License-Identifier: MIT
"""
from functools import wraps
from typing import Any, Callable

import typer

from expand import expand_kwargs, make_signature

__all__ = ["typer"]


def engorgio(*, typer: bool = False) -> Callable:
    """Expand Pydantic keyword arguments.

    Decorator function to expand arguments of pydantic models to accept the
    individual fields of Models.
    """

    def decorator(func: Callable) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **expand_kwargs(func, kwargs))

        return make_signature(func, wrapper, typer=typer)

    return decorator
