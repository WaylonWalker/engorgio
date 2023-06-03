"""Models defines a set of classes for representing people and their hair.

Classes:

* `Alpha`: A class for representing an alpha value.
* `Color`: A class for representing a color.
* `Hair`: A class for representing hair.
* `Person`: A class for representing a person.

"""

import datetime
from typing import Optional

from polyfactory.factories.pydantic_factory import ModelFactory
from pydantic import BaseModel, Field


class Alpha(BaseModel):

    """A class for representing an alpha value."""

    a: int = Field(
        ...,
        description="The alpha value.",
    )


class Color(BaseModel):

    """A class for representing a color."""

    r: int = Field(
        ...,
        description="The red component of the color.",
    )
    g: int = Field(
        ...,
        description="The green component of the color.",
    )
    b: int = Field(
        ...,
        description="The blue component of the color.",
    )
    alpha: Alpha = Field(
        ...,
        description="The alpha value of the color.",
    )


class Hair(BaseModel):

    """A class for representing hair."""

    color: Color = Field(
        ...,
        description="The color of the hair.",
    )
    length: int = Field(
        ...,
        description="The length of the hair.",
    )


class Person(BaseModel):

    """A class for representing a person."""

    name: str = Field(
        ...,
        description="The name of the person.",
    )
    alias: Optional[str] = Field(
        None,
        description="An optional other name for the person.",
    )
    age: int = Field(
        ...,
        description="The age of the person.",
    )
    email: Optional[str] = Field(
        None,
        description="An optional email address for the person.",
    )
    pet: str = Field(
        "dog",
        description="The person's pet.",
    )
    address: str = Field(
        "123 Main St",
        description="Where the person calls home.",
    )
    hair: Hair = Field(
        ...,
        description="The person's hair.",
    )


class AlphaFactory(ModelFactory[Alpha]):

    """A class for generating an alpha value."""

    __model__ = Alpha


class ColorFactory(ModelFactory[Color]):

    """A class for generating a color."""

    __model__ = Color


class HairFactory(ModelFactory[Hair]):

    """A class for generating hair."""

    __model__ = Hair


class PersonFactory(ModelFactory[Person]):

    """A class for generating a person."""

    __model__ = Person


class MyDate(BaseModel):
    date: datetime.datetime


class DateFactory(ModelFactory[MyDate]):
    __model__ = MyDate
