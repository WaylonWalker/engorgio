"""Condense parameters back into models.

SPDX-FileCopyrightText: 2023-present Waylon S. Walker <waylon@waylonwalker.com>

SPDX-License-Identifier: MIT
"""
import inspect
from typing import Any, Callable, Dict, Optional


def get_kwargs_for_param(
    param: inspect.Parameter,
    kwargs: Dict,
    model_separator: str = "__",
):
    """Get kwargs for the param from the dict of kwargs."""
    min_kwargs = 2
    model_kwargs = {k: v for k, v in kwargs.items() if len(k.split("__")) >= min_kwargs}
    return {
        k.split(model_separator)[-1]: v
        for k, v in model_kwargs.items()
        if k.split(model_separator)[-2] == param.name
    }


def expand_param(
    param: inspect.Parameter,
    kwargs: Dict[str, Any],
    models: Optional[Dict[str, str]] = None,
    model_separator: str = "__",
    *,
    include_parent_model: bool = True,
) -> Any:
    """Further expands params with a Pydantic annotation, given a param.

    Recursively creates an instance of any param.annotation that has __fields__
    """
    if models is None:
        models = {}

    for field_name, field in param.annotation.__fields__.items():
        if hasattr(field.annotation, "__fields__"):
            models[field_name] = expand_param(
                param=field,
                kwargs=kwargs,
                models=models,
                include_parent_model=include_parent_model,
            )
    if include_parent_model:
        param_kwargs = get_kwargs_for_param(
            param=param,
            kwargs=kwargs,
            model_separator=model_separator,
        )
    else:
        param_kwargs = kwargs
    return param.annotation(**param_kwargs, **models)


def condense_instances(
    func: Callable,
    kwargs: Dict[str, Any],
    model_separator: str = "__",
    *,
    include_parent_model: bool = True,
) -> Dict[str, Any]:
    """Condense expanded kwargs back to model instances.

    Inspects the arguments of the func and expands any of the kwargs with a
    Pydantic annotation, to add its fields to the kwargs.
    """
    sig = inspect.signature(func)
    updated_kwargs = {}
    for name, value in kwargs.items():
        if name in sig.parameters:
            updated_kwargs[name] = value

    for name, param in sig.parameters.items():
        # func wants this directly
        # this should check isinstance, but it's not working
        #
        if name in kwargs and repr(param.annotation) == repr(kwargs[name]):
            updated_kwargs[name] = kwargs[name]

        # an instance was not passed in, create one with kwargs passed in
        elif hasattr(param.annotation, "__fields__"):
            updated_kwargs[name] = expand_param(
                param=param,
                kwargs=kwargs,
                model_separator=model_separator,
                include_parent_model=include_parent_model,
            )
        # its something else so pass it
    return updated_kwargs
