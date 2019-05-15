import json
import os
import typing
from distutils.util import strtobool

import ruamel.yaml

from .constants import REQUIRED, CastTypes


def load_config(path: str) -> dict:
    """
    Given a file path, parse it based on its extension (YAML or JSON)
    and return the values as a Python dictionary. JSON is the default if an
    extension can't be determined.
    """
    __, ext = os.path.splitext(path)
    if ext in [".yaml", ".yml"]:
        loader = ruamel.yaml.safe_load
    else:
        loader = json.load
    with open(path) as f:
        return loader(f) or {}


class EnvLoader:
    def __call__(
        self, key: str, default: typing.Any, cast: typing.Optional[CastTypes] = None
    ) -> typing.Any:
        value = os.environ[key]
        if not cast:
            if default is not None and default is not REQUIRED:
                cast = type(default)
            else:
                cast = str
        try:
            return getattr(self, "cast_{}".format(cast.__name__.lower()))(value)
        except AttributeError:
            return cast(value)

    def cast_list(self, val: str) -> list:
        """Convert a comma-separated string to a list"""
        return val.split(",")

    def cast_bool(self, val: str) -> bool:
        """
        True values are y, yes, t, true, on and 1
        False values are n, no, f, false, off and 0
        Raises ValueError if val is anything else.
        """
        return bool(strtobool(val))

    def __contains__(self, key):
        return key in os.environ


env = EnvLoader()
