"""
Copyright (C) J Leadbetter <j@jleadbetter.com>
Affero GPL v3
"""

import configparser
import importlib
import os
import sys
from typing import Any, Optional

from common.stores.settings import SettingsStore
from common.utils.singleton import Singleton


class AdapterInitializationError(Exception):
    pass


class AdapterNotFoundError(Exception):
    pass


class AdapterStore(metaclass=Singleton):
    """
    Singleton that instantiates all adapters using the specified config
    """

    def __init__(
        self,
        config: Optional[str]=None,
        subsection: Optional[str]=None,
    ):
        """
        :config: setup.cfg to use to create adapters
        :subsection: subsection of setup.cfg to use for settings
        """
        self._adapters = {}
        self._settings = SettingsStore(config, subsection)
        self.initialize()

    def _get_adapter_cls(self, port_name: str):
        module_name, cls_name = self._settings.get('ports', port_name).rsplit('.', 1)
        module = importlib.import_module(module_name)
        AdapterCls = getattr(module, cls_name)
        return AdapterCls

    def initialize(self, force: bool=False):
        """
        Initialize adapters for use in the app.

        This is done as a separate step from __init__
        so we can troubleshoot individual adapter initializations.

        :force: Re-import the adapters.
            If false, ignores build if adapters already exist.
        """

        if force:
            self._adapters = {}

        ports = self._settings.get('ports')
        exceptions = {}
        for port in ports:
            # Don't override existing adapters
            if port in self._adapters:
                continue

            try:
                AdapterCls = self._get_adapter_cls(port)
                adapter_options = {}
                for key in self._settings.get('adapters.common', {}):
                    value = self._settings.get('adapters.common', key)
                    adapter_options[key] = value

                custom_options_section = f'adapters.{port}'
                section = self._settings.get(custom_options_section)
                if section:
                    for key in section:
                        value = self._settings.get(section, key)
                        adapter_options[key] = value

                adapter = AdapterCls(**adapter_options)
                self._adapters[port] = adapter
            except Exception as exc:
                exceptions[port] = exc

        if exceptions:
            raise AdapterInitializationError(str(exceptions))

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
