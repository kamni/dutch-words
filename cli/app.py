"""
Copyright (C) J Leadbetter <j@jleadbetter.com>
Affero GPL v3
"""

import os
import sys

from textual.app import App

from common.stores.adapter import AdapterStore
from common.stores.auth import AuthStore

from .views.app_settings import AppSettingsScreen
from .views.edit import EditScreen
from .views.learn import LearnScreen
from .views.login import LoginScreen
from .views.registration import RegistrationScreen
from .views.upload import UploadScreen


class TenThousandWordsApp(App):
    """
    CLI app for the 10,000 Words project
    """

    SCREENS = {
        'app_settings': AppSettingsScreen,
        'edit': EditScreen,
        'learn': LearnScreen,
        'login': LoginScreen,
        'registration': RegistrationScreen,
        'upload': UploadScreen,
    }

    def on_mount(self):
        self._auth = AuthStore()
        self._adapters = AdapterStore()

        self.theme = 'flexoki'

        # First time using the app
        if self._login_not_configured:
            self.push_screen('login')
            self.push_screen('app_settings')
        else:
            self.push_screen('login')

    def _login_not_configured(self):
        return self._auth.get(AuthStore.IS_CONFIGURED)
