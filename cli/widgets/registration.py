"""
Copyright (C) J Leadbetter <j@jleadbetter.com>
Affero GPL v3
"""

from pathlib import Path

from textual.app import ComposeResult
from textual.containers import Center, Container
from textual.widgets import Button, Input, Static

from common.stores.adapter import AdapterStore


class RegistrationWidget(Container):
    """
    Register a new user
    """

    CSS_PATH = [
        (Path(__file__).resolve().parent / 'css' / 'registration.tcss').as_posix(),
    ]

    @property
    def settings(self):
        if not hasattr(self, '_settings') or self._settings is None:
            adapters = AdapterStore()
            self._settings = adapters.get('AppSettingsPort')
        return self._settings

    @property
    def userdb_adapter(self):
        if not hasattr(self, _userdb_adapter) or self._userdb_adapter is None:
            adapters = AdapterStore()
            self._userdb_adapter = adapters.get('UserDBPort')
        return self._userdb_adapter

    def compose(self) -> ComposeResult:
        yield Center(
            Center(
                Static('Create a New User', id='registration-text'),
                id='registration-text-wrapper',
            ),
            Center(
                Input(placeholder='Username', id='username-input'),
                Input(placeholder='Password', password=True, id='password-input'),
                id='registration-input-wrapper',
            ),
            Center(
                Button('Create User', variant='primary', id='registration-button'),
                id='registration-button-wrapper',
            ),
            id='registration-wrapper',
        )

    def on_button_pressed(self, event: Button.Pressed):
        event.button.disabled = True
        # TODO: re-enable if validation errors
        # TODO: save user

    def on_mount(self):
        first_field = self.query_one('#username-input')
        first_field.focus()

        settings = self.settings.get()
        if settings and settings.passwordless_login:
            password_field = self.query_one('#password-input')
            password_field.display = 'none'
