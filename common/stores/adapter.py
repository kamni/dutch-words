"""
Copyright (C) J Leadbetter <j@jleadbetter.com>
Affero GPL v3
"""

import configparser
import importlib
import os
import sys
from typing import Any

from common.utils.singleton import Singleton


TOP_LEVEL_FOLDER = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        '..',
        '..',
    ),
)
DEFAULT_CONFIG = 'config.ini'


class AdapterNotFoundError(Exception):
    pass


class AdapterStore(metaclass=Singleton):
    """
    Singleton that instantiates all adapters using the specified config
    """

    _adapters = {}

    def __init__(self, config: str=DEFAULT_CONFIG):
        self.config_file = os.path.join(TOP_LEVEL_FOLDER, config)
        self.config = configparser.ConfigParser()
        self.config.read(self.config_file)

    def initialize(self, force_rebuild: bool=False):
        """
        Initialize adapters for use in the app.
        The method

        :force_rebuild: Re-import the adapters.
            If false, ignores build if adapters already exist.
        """

        if force_rebuild:
            self._adapters = {}

        ports = self.config['ports']
        for port in ports:
            # Don't override existing adapters
            if port in self._adapters:
                continue

            module_name, cls_name = self.config['ports'][port].rsplit('.', 1)
            module = importlib.import_module(module_name)
            AdapterCls = getattr(module, cls_name)

            adapter_options = {
                key: value
                for (key, value) in self.config['adapters.common'].items()
            }
            custom_options_section = f'adapters.{port}'
            if custom_options_section in self.config.sections():
                for (key, value) in self.config[f'adapters.{port}']:
                    adapter_options[key] = value

            adapter = AdapterCls(**adapter_options)
            self._adapters[port] = adapter

    def get(self, port_name: str) -> Any:
        """
        Return the expected adapter base

        :port_name: name of the port class (e.g., 'AuthnPort')

        :return: the configured adapter for the port
        :raise: AdapterNotFoundError, if port is not configured
        """

        try:
            adapter = self._adapters[port_name.lower()]
        except KeyError:
            raise AdapterNotFoundError(
                f'Unable to find adapter for {port_name}. '
                'Did you call AdapterStore.initialize first?'
            )

        return adapter
