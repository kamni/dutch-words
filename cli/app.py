"""
Copyright (C) J Leadbetter <j@jleadbetter.com>
Affero GPL v3
"""

import os
import sys

from textual.app import App
from textual.reactive import reactive

from common.stores.auth import AuthStore

from .views.edit import EditScreen, UploadModal
from .views.learn import LearnScreen
from .views.login import FirstTimeModal, LoginScreen, RegistrationModal
from .views.settings import PermissionDenied, SettingsScreen


class TenThousandWordsApp(App):
    """
    CLI app for the 10,000 Words project
    """

    BINDINGS = [
        ('q', 'logout', 'Log Out'),
    ]

    MODES = {
        'edit': EditScreen,
        'learn': LearnScreen,
        'login': LoginScreen,
        'settings': AppSettingsScreen,
    }

    SCREENS = {
        'first_time': FirstTimeModal,
        'permission_denied': PermissionDeniedModal,
        'register': RegistrationModal,
        'upload': UploadModal,
    }

    current_user = reactive(None)

    @property
    def auth(self):
        if not hasattr(self, '_auth') or self._auth is None:
            self._auth = AuthStore()
        return self._auth

    @property
    def admin_bindings(self):
        bindings = [
            ('s', 'settings', 'Settings')
            ('e', 'edit', 'Edit'),
            ('l', 'learn', 'Learn'),
            ('q', 'logout', 'Log Out'),
        ]
        return bindings

    @property
    def is_admin_session(self):
        return self.auth.logged_in_user and self.auth.logged_in_user.is_admin

    @property
    def minimal_bindings(self):
        bindings = [
            ('q', 'logout', 'Log Out'),
        ]
        return bindings

    @property
    def standard_bindings(self):
        bindings = [
            ('e', 'edit', 'Edit'),
            ('l', 'learn', 'Learn'),
            ('q', 'logout', 'Log Out'),
        ]
        return bindings

    def on_mount(self):
        self.theme = 'flexoki'

        if self.auth.logged_in_user:
            self.action_edit()

        self.action_login()

    def action_edit(self):
        if not self.auth.logged_in_user:
            return self.action_login()

        self.set_bindings()
        self.switch_mode('edit')

    def action_learn(self):
        if not self.auth.logged_in_user:
            return self.action_login()

        self.set_bindings()
        self.switch_mode('learn')

    def action_login(self):
        self.set_bindings(minimal=True)
        self.switch_mode('login', self.update_current_user)

        if not self.auth.is_configured:
            self.push_screen('first_time')

    def action_logout(self):
        self.auth.logout()
        self.update_current_user()
        self.switch_mode('login')

    def action_settings(self):
        if not self.auth.is_configured:
            self.set_bindings(minimal=True)
            return self.switch_mode('settings')

        user = self.auth.logged_in_user
        if not user:
            self.action_login()
        elif not user.is_admin:
            self.push_screen('permission_denied')
        else:
            self.set_bindings(minimal=True)
            self.switch_mode('settings')

    def set_bindings(self, minimal=False):
        if minimal:
            self.BINDINGS = self.minimal_bindings
        elif self.is_admin_session:
            self.BINDINGS = self.admin_bindings
        else:
            self.BINDINGS = self.standard_bindings

    def update_current_user(self):
        self.current_user = self.auth.logged_in_user

    def watch_current_user(self):
        settings_bindings = ('s', 'settings', 'Settings')
        if self.current_user and self.current_user.is_admin:
            if settings_bindings not in self.BINDINGS:
                self.BINDINGS.insert(0, settings_bindings)
        else:
            if settings_bindings in self.BINDINGS:
                self.BINDINGS.pop(self.BINDING.index(settings_bindings))
