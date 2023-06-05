"""Example usage of engorgio with the Person model.

SPDX-FileCopyrightText: 2023-present Waylon S. Walker <waylon@waylonwalker.com>

SPDX-License-Identifier: MIT
"""
from typer import Typer

from engorgio import engorgio
from tests.models import Hero, Person

app = Typer()


@engorgio()
def get_person(person: Person, thing: str = None) -> Person:
    """Mydocstring."""
    return person


@engorgio()
def get_hero(hero: Hero) -> Hero:
    """Mydocstring."""
    return hero
