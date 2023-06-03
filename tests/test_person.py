"""Example usage of engorgio with the Person model.

SPDX-FileCopyrightText: 2023-present Waylon S. Walker <waylon@waylonwalker.com>

SPDX-License-Identifier: MIT
"""

import inspect

import pytest

from engorgio import engorgio

from . import models

# this one is broken
# def test_no_pydantic() -> None:
#     @engorgio()
#     def get_person(alpha) -> None:
#         """Mydocstring."""


def test_single_signature() -> None:
    @engorgio()
    def get_person(alpha: models.Alpha) -> None:
        """Mydocstring."""
        return alpha

    sig = inspect.signature(get_person)
    params = sig.parameters
    assert "a" in params

    assert "alpha" not in params
    alpha = models.AlphaFactory().build()
    assert get_person(**alpha.dict()) == alpha


@pytest.mark.parametrize(
    "alpha",
    models.AlphaFactory().batch(size=5),
)
def test_single_instance(alpha: models.Alpha) -> None:
    @engorgio()
    def get_person(alpha: models.Alpha) -> None:
        """Mydocstring."""
        return alpha

    assert get_person(**alpha.dict()) == alpha
    # this should maybe work


def test_one_nest_signature() -> None:
    @engorgio()
    def get_person(color: models.Color) -> None:
        """Mydocstring."""
        return color

    sig = inspect.signature(get_person)
    params = sig.parameters
    assert "r" in params
    assert "g" in params
    assert "b" in params
    assert "a" in params

    assert "color" not in params
    assert "alpha" not in params

    color = models.ColorFactory().build()
    assert get_person(**color.dict(exclude={"alpha"}), **color.alpha.dict()) == color


@pytest.mark.parametrize(
    "color",
    models.ColorFactory().batch(size=5),
)
def test_one_nest_instance(color: models.Color) -> None:
    @engorgio()
    def get_person(color: models.Color) -> None:
        """Mydocstring."""
        return color

    assert get_person(**color.dict(exclude={"alpha"}), **color.alpha.dict()) == color


def test_two_nest_signature() -> None:
    @engorgio()
    def get_hair(hair: models.Hair) -> None:
        """Mydocstring."""
        return hair

    sig = inspect.signature(get_hair)
    params = sig.parameters
    assert "length" in params
    assert "r" in params
    assert "g" in params
    assert "b" in params
    assert "a" in params

    assert "hair" not in params
    assert "color" not in params
    assert "alpha" not in params

    hair = models.HairFactory().build()
    assert (
        get_hair(
            **hair.dict(exclude={"color"}),
            **hair.color.dict(exclude={"alpha"}),
            **hair.color.alpha.dict(),
        ) ==
        hair
    )


@pytest.mark.parametrize(
    "hair",
    models.HairFactory().batch(size=5),
)
def test_two_nest_instance(hair: models.Hair) -> None:
    @engorgio()
    def get_hair(hair: models.Hair) -> None:
        """Mydocstring."""
        return hair

    assert (
        get_hair(
            **hair.dict(exclude={"color"}),
            **hair.color.dict(exclude={"alpha"}),
            **hair.color.alpha.dict(),
        ) ==
        hair
    )


def test_three_nest_signature() -> None:
    @engorgio()
    def get_person(person: models.Person) -> None:
        """Mydocstring."""
        return person

    sig = inspect.signature(get_person)
    params = sig.parameters
    assert "name" in params
    assert "alias" in params
    assert "age" in params
    assert "email" in params
    assert "pet" in params
    assert "address" in params
    assert "length" in params
    assert "r" in params
    assert "g" in params
    assert "b" in params
    assert "a" in params

    assert "person" not in params
    assert "hair" not in params
    assert "color" not in params
    assert "alpha" not in params

    person = models.PersonFactory().build()
    assert (
        get_person(
            **person.dict(exclude={"hair"}),
            **person.hair.dict(exclude={"color"}),
            **person.hair.color.dict(exclude={"alpha"}),
            **person.hair.color.alpha.dict(),
        ) ==
        person
    )


@pytest.mark.parametrize(
    "person",
    models.PersonFactory().batch(size=5),
)
def test_three_nest_instance(person: models.Person) -> None:
    @engorgio()
    def get_person(person: models.Person) -> None:
        """Mydocstring."""
        return person

    assert (
        get_person(
            **person.dict(exclude={"hair"}),
            **person.hair.dict(exclude={"color"}),
            **person.hair.color.dict(exclude={"alpha"}),
            **person.hair.color.alpha.dict(),
        ) ==
        person
    )
