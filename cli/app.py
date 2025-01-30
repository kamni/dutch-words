"""
Copyright (C) J Leadbetter <j@jleadbetter.com>
Affero GPL v3
"""

import os
import sys

from textual.app import App

from common.stores.adapter import AdapterStore
from common.stores.auth import AuthStore

from .views.login import LoginScreen


class TenThousandWordsApp(App):
    """
    CLI app for the 10,000 Words project
    """

    def on_mount(self):
        self._auth = AuthStore()
        self._adapters = AdapterStore()

        self.theme = 'flexoki'

        self.install_screen(LoginScreen, 'login')
        self.push_screen('login')
