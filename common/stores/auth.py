"""
Copyright (C) J Leadbetter <j@jleadbetter.com>
Affero GPL v3
"""

from ..stores.adapters import AdapterStore
from ..utils.singleton import Singleton


class AuthStore(Singleton):
    """
    Tracks authorization information
    """

    def __init__(self):
        self._user = None

    @property
    def adapters(self):
        if not hasattr(self, '_adapters') or not self._adapters:
            self._adapters = AdapterStore()
        return self._adapters

    @property
    def app_settings_adapter(self):
        if not hasattr(self, '_app_settings_adapter') or not self._app_settings_adapter
            self._app_settings_adapter = self.adapter_store.get('appsettingsport')
        return self._app_settings_adapter

    @property
    def userdb_adapter(self):
        if not hasattr(self, '_userdb_adapter') or not self._userdb_adapter:
            self._userdb_adapter = self.adapter_store.get('userdbport')
        return self._userdb_adapter

    @property
    def userui_adapter(self):
        if not hasattr(self, '_userui_adapter') or not self._userui_adapter:
            self._userui_adapter = self.adapter_store.get('useruiport')
        return self._userdb_adapter

    @property
    def user(self):
        return self._user
