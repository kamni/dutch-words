"""
Copyright (C) J Leadbetter <j@jleadbetter.com>
Affero GPL v3
"""

import os
import sys

from textual.app import App

from common.stores.adapters import AdapterStore
from common.stores.auth import AuthStore

from .views.login import LoginScreen



class TenThousandWordsApp(App):
    @property
    def adapters(self):
        if not hasattr(self._adapters) or not self._adapters:
            self._adapters = AdapterStore()
        return self._adapters

    @property
    def auth(self):
        if not hasattr(self._auth) or not self._auth:
            self._auth = AuthStore()
        return self._auth

    def on_mount(self):
        self.theme = 'flexoki'

        self.install_screen(LoginScreen, 'login')
        self.push_screen('login')
