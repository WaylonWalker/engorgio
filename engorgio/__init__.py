"""
Engorgio expands python function arguments.

Write python functions that accept pydantic models as arguments,
and `engorgio` will expand these arguments to accept each field
individually and give you an instance of your model to use in your
function.
SPDX-FileCopyrightText: 2023-present Waylon S. Walker <waylon@waylonwalker.com>

SPDX-License-Identifier: MIT
"""

from .decorator import engorgio

__all__ = ["engorgio"]
