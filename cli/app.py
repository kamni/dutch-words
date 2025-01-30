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

    BINDINGS = [
        ('e', 'app.switch_mode("edit")', 'Edit'),
        ('l', 'app.switch_mode("learn")', 'Learn'),
        ('s', 'app.switch_mode("settings")', 'Settings'),
        ('q', 'logout', 'Log Out'),
    ]

    MODES = {
        'edit': EditScreen,
        'learn': LearnScreen,
        'login': LoginScreen,
        'settings': SettingsScreen,
    }

    SCREENS = {
        'upload': UploadScreen,
        'register': RegistrationScreen,
    }

    @property
    def auth(self):
        if not hasattr(self, '_auth') or self._auth is None:
            adapters = AdapterStore()
            self._auth = adapters.get('AuthPort')
        return self._auth

    def on_mount(self):
        self.theme = 'flexoki'

        if not self.auth.is_configured:
            self.switch_mode('settings')
        else:
            self.switch_mode('login')

    def action_logout(self):
        self.auth.logout()
        # TODO: Need to pop all other screens
        self.switch_mode('login')
