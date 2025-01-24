"""
Copyright (C) J Leadbetter <j@jleadbetter.com>
Affero GPL v3
"""

import configparser
import os
from typing import Any, Optional

from common.utils.singleton import Singleton


TOP_LEVEL_FOLDER = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        '..',
        '..',
    ),
)
DEFAULT_CONFIG = os.path.join(TOP_LEVEL_FOLDER, 'config.ini')


class SettingsStore(metaclass=Singleton):
    """
    Store global settings that are available across all parts of the app
    """

    def __init__(self, config: str=DEFAULT_CONFIG):
        self._config = configparser.ConfigParser()
        self._config.read(config)

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

    def get(
        self,
        section: str,
        key: Optional[str]=None,
        value_type: Optional[type]=str,
    ) -> Any:
        """
        Retrieve a setting from the config file.

        :section: [section.name] of the configuration file.
        :key: key from the section.
            If not specified, only the section is returned.
        :type: Python type to return.
            Defaults to a string.

        :return: either section of the config (list), or value, if found;
            otherwise None
        """

        # Configparse lower-cases all strings,
        # even if the config uses camelCase
        section_name = section.lower()
        try:
            section = self._config[section]
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
