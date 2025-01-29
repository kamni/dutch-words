"""
Copyright (C) J Leadbetter <j@jleadbetter.com>
Affero GPL v3
"""

import configparser
from pathlib import Path
from typing import Any, Optional

from common.utils.singleton import Singleton


BASE_DIR = Path(__file__).resolve().parent.parent.parent
DEFAULT_CONFIG = BASE_DIR / 'setup.cfg'


class SettingsStore(metaclass=Singleton):
    """
    Store global settings that are available across all parts of the app
    """

    def __init__(
        self,
        config: Optional[str]=None,
        subsection: Optional[str]=None,
    ):
        """
        :config: Configuration file to use.
            Defaults to config.ini in the top-level project folder

        :subsection: Subsection of the config.ini file to use.
            Example: dev.json or dev.django.
            If not specified, uses the config.meta.DefaultConfig setting.
            Please look at the config.ini file for configuration optiions.
        """
        self._config_name = config or DEFAULT_CONFIG
        self._subsection_name = subsection

        self._config = {}
        self._subsection = ''
        self.initialize()

    @property
    def name(self):
        return self._config['config.meta']['name']

    @property
    def subsection(self):
        return self._config['config.meta']['defaultconfig']

    def _convert_to_type(self, value: str, value_type: type):
        if value_type == bool:
            value = value.lower()
            if value in ['yes', 'y', '1', 'true']:
                return True
            elif value in ['no', 'n', '0', 'false']:
                return False
            else:
                return None
        else:
            return value_type(value)

    def _get_ini_path(self, subpath: str):
        return f'{self._subsection}.{subpath}'

    def initialize(self, force=False):
        """
        Initialize this store.
        If it has already been initialized,
        this will skip initialization.

        :force: Force re-initialization
        """
        if self._config and not force:
            return

        self._config = configparser.ConfigParser()
        self._config.read(self._config_name)
        self._subsection = (
            self._subsection_name or self._config['config.meta']['defaultconfig']
        )

    def get(
        self,
        section: str,
        key: Optional[str]=None,
        value_type: Optional[type]=str,
    ) -> Any:
        """
        Retrieve a setting from the config file.

        :section: relevant section of the configuration file.
            This is relative to the config_subsection specified in the init.
            E.g. 'ports' to get '[dev.json.ports]'.
        :key: key from the section.
            If not specified, the whole section is returned.
        :type: Python type to return.
            Defaults to a string.

        :return: either section of the config (list), or value, if found;
            otherwise None
        """

        # Configparse lower-cases all strings,
        # even if the config uses camelCase
        section_name = section.lower()
        try:
            section_path = self._get_ini_path(section)
            section = self._config[section_path]
        except KeyError:
            return None

        if not key:
            return list(section)

        # Configparse lower-cases all strings,
        # even if the config uses camelCase
        key = key.lower()
        try:
            config_value = section[key]
            value = self._convert_to_type(config_value, value_type)
        except (KeyError, ValueError):
            value = None

        return value
