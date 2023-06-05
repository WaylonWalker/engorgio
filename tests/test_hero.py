"""
Hero has a Pet, both have a name.  These tests assert the names don't get
mixed.

SPDX-FileCopyrightText: 2023-present Waylon S. Walker <waylon@waylonwalker.com>

SPDX-License-Identifier: MIT
"""

import inspect

from engorgio import engorgio
from tests import models


def test_make_hero():
    @engorgio(include_parent_model=True)
    def get_hero(hero: models.Hero) -> models.Hero:
        """Mydocstring."""
        return hero

    sig = inspect.signature(get_hero)
    params = sig.parameters
    assert "hero__name" in params
    assert "hero__pet__name" in params

    assert "name" not in params
    assert "pet__name" not in params

    hero = models.HeroFactory().build()
    assert get_hero(hero__name=hero.name, hero__pet__name=hero.pet.name) == hero
