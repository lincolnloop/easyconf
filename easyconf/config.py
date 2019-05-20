import functools
import logging
import os
import typing

from .constants import REQUIRED, CastTypes
from .generators.gitignore import update_gitignore
from .generators.yaml import YAMLGenerator
from .loader import env, load_config

logger = logging.getLogger(__file__)


class RequiredConfigVarMissing(Exception):
    def __init__(self, key):
        self.key = key


class Config:
    def __init__(
        self,
        default_files: typing.Optional[typing.Union[str, typing.List[str]]] = None,
        *,
        file_env_var: typing.Optional[str] = None,
        generate: bool = True,
    ):
        self._loaded = False
        self._creating = None
        # Check for files
        if file_env_var:
            env_filename = os.environ.get(file_env_var)
            if env_filename:
                default_files = env_filename
        if not default_files:
            default_files = []
        elif isinstance(default_files, str):
            default_files = [default_files]
        self._config = {}
        for filename in default_files:
            if os.path.exists(filename):
                self._load(filename)
                break
        # No match? Try to open file for write.
        if not self._loaded and default_files and generate:
            logger.warning("No configuration files found, attempting to create one...")
            for filename in default_files:
                try:
                    self._creating = YAMLGenerator(filename)
                    logger.warning(f"Creating {filename} configuration file")
                    update_gitignore(filename)
                except OSError:
                    continue
            if not self._creating:
                logger.warning("Could not create a configuration file")

    def _load(self, filename: str):
        self._config = load_config(filename)
        self._loaded = True

    def __getattr__(self, key):
        return functools.partial(self._get_config_var, key)

    def _get_config_var(
        self,
        key: str,
        default: typing.Any = REQUIRED,
        *,
        cast: typing.Optional[CastTypes] = None,
        initial: typing.Optional[typing.Callable[[], CastTypes]] = None,
        help: typing.Optional[str] = None,
    ):
        if self._creating and key not in self._config:
            if initial is None:
                if cast:
                    default = cast(default)
                self._creating.add_commented(key, default, help)
                self._config[key] = default
            else:
                if callable(initial):
                    initial = initial()
                self._creating.add(key, initial, help)
                self._config[key] = initial

        if key in env:
            return env(key, default, cast)

        if key in self._config:
            value = self._config[key]
            if cast and getattr(cast, "cast_from_config", False):
                value = cast(value)
        else:
            value = default
            if cast:
                value = cast(value)

        if value is REQUIRED:
            raise RequiredConfigVarMissing(key)

        return value
