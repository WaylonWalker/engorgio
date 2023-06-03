"""
Engorgio expands python function arguments.

Write python functions that accept pydantic models as arguments,
and `engorgio` will expand these arguments to accept each field
individually and give you an instance of your model to use in your
function.
"""

from .decorator import engorgio

__all__ = ["engorgio"]
