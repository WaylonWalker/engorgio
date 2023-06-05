"""engorgio.

SPDX-FileCopyrightText: 2023-present Waylon S. Walker <waylon@waylonwalker.com>

SPDX-License-Identifier: MIT
"""
from functools import wraps
from typing import Any, Callable

import typer

from engorgio.condense import condense_instances
from engorgio.expand import make_expanded_function

__all__ = ["typer"]


def engorgio(
    *,
    model_separator: str = "__",
    include_parent_model: bool = True,
    typer: bool = False,
) -> Callable:
    """Expand Pydantic keyword arguments.

    Decorator function to expand arguments of pydantic models to accept the
    individual fields of Models.
    """

    def decorator(func: Callable) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(
                *args,
                **condense_instances(
                    func=func,
                    kwargs=kwargs,
                    model_separator=model_separator,
                    include_parent_model=include_parent_model,
                ),
            )

        return make_expanded_function(
            func=func,
            wrapper=wrapper,
            include_parent_model=include_parent_model,
            model_separator=model_separator,
            typer=typer,
        )

    return decorator
