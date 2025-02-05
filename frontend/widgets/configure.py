"""
Copyright (C) J Leadbetter <j@jleadbetter.com>
Affero GPL v3
"""

import time
from typing import Optional

from nicegui import ui
from nicegui.elements.label import Label

from common.models.app import AppSettingsDB
from frontend.widgets.base import BaseWidget


class OptionWidget(BaseWidget):
    """
    Display an individual configuration option
    """

    def __init__(self, text: str, value: bool):
        super().__init__()

        self._text = text
        self._value = value

    @property
    def value(self) -> bool:
        return self.switch.value

    def display(self):
        def update_no_and_yes():
            value = self.switch.value
            no = self.no
            yes = self.yes

            if value:
                yes.classes(add='outline')
                no.classes(remove='outline')
            else:
                no.classes(add='outline')
                yes.classes(remove='outline')

        ui.label(self._text)
        self.no = ui.label('no').classes('text-right text-amber-600 px-4')
        self.switch = ui.switch(
            value=self._value,
            on_change=update_no_and_yes,
        )
        self.yes = ui.label('yes').classes('text-left text-green-600 px-4')

        update_no_and_yes()


class ConfigureWidget(BaseWidget):
    """
    Configure the global app settings
    """

    def __init__(self, redirect_after_save: Optional[str]='/'):
        super().__init__()
        self._redirect = redirect_after_save

    def display(self):
        adapter = self._adapters.get('AppSettingsDBPort')
        current_settings = adapter.get_or_default()

        self._multiuser = OptionWidget(
            'Can multiple people use the app?',
            current_settings.multiuser_mode,
        )
        self._passwordless = OptionWidget(
            'Log in without a password?',
            current_settings.passwordless_login,
        )
        self._show_users = OptionWidget(
            'Show user list on the login page?',
            current_settings.show_users_on_login_screen,
        )

        def save_settings():
            settings = AppSettingsDB(
                multiuser_mode=self._multiuser.value,
                passwordless_login=self._passwordless.value,
                show_users_on_login_screen=self._show_users.value,
            )
            adapter.create_or_update(settings)
            self._app_settings.initialize(force=True)
            ui.notify('Settings Saved!')
            time.sleep(1)
            self.emit_done()

        with ui.card().classes('absolute-center'):
            ui.label('Settings').classes('text-3xl')
            ui.separator()

            with ui.grid(columns='auto auto auto auto'):
                self._multiuser.display()
                self._passwordless.display()
                self._show_users.display()

            ui.separator()
            ui.button('Save', on_click=save_settings).classes('self-center')
