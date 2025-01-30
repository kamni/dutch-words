"""
Copyright (C) J Leadbetter <j@jleadbetter.com>
Affero GPL v3
"""

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Button, Footer

from common.stores.adapter import AdapterStore


# To be replaced by screen content
class TempButton(Button):
    pass


class AppSettingsScreen(Screen):
    """
    Manage the settings for the app
    """

    BINDINGS = [
        ('s', 'save', 'Save'),
        ('escape', 'app.pop_screen', 'Cancel'),
    ]

    @property
    def app_settings(self):
        if not hasattr(self, '_app_settings') or self._app_settings is None:
            adapters = AdapterStore()
            self._app_settings = adapters.get('AppSettingsPort')
        return self._app_settings

    @property
    def auth(self):
        if not hasattr(self, '_auth') or self._auth is None:
            adapters = AdapterStore()
            self._auth = adapters.get('AuthPort')
        return self._auth

    def action_save(self):
        pass

    def compose(self) -> ComposeResult:
        #if self._can_edit_settings():
        # Check if user not allowed...then pop if not

        # Just a quick setup:
        # Suggested configurations:
        # Desktop user: False, True, False
        # Web user: True, False, False
        # Paranoid: False, False, False
        # Trusting: True, True, True

        # Explicit Save/Cancel buttons
        # If no settings

        # if not configured, do everything
        # if user and not user.is_admin
        # switch back to login

        # Welcome to 10,000 Words
        # Configure the app; if unsure, keep default settings
        # More than one user (yes/no), default no
        # Automatically log in (yes/no), default yes
        # - when set to no, show third option
        # - Show users on the login screen or Show your user on the login screen,
        #   if not more than one user
        yield TempButton("Configure", variant="primary")
        yield Footer()
