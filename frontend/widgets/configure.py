"""
Copyright (C) J Leadbetter <j@jleadbetter.com>
Affero GPL v3
"""

from nicegui import ui

from frontend.widgets.base import BaseWidget


class ConfigureWidget(BaseWidget):
    """
    Configure the global app settings
    """

    def display(self):
        def save_settings():
            ui.notify('Work in progress')

        app_settings = self._adapters.get('AppSettingsDBPort').get_or_default()

        with ui.card().classes('absolute-center'):
            with ui.row():
                ui.label('Can multiple people use the app?')
                ui.label('no')
                ui.switch(value=app_settings.multiuser_mode)
                ui.label('yes')
            with ui.row():
                ui.label('Log in without a password?')
                ui.label('no')
                ui.switch(value=app_settings.passwordless_login)
                ui.label('yes')
            with ui.row():
                ui.label('Show user list on the login page?')
                ui.label('yes')
                ui.switch(value=app_settings.show_users_on_login_screen)
                ui.label('no')

            ui.button('Save', on_click=save_settings)
