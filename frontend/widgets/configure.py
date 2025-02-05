"""
Copyright (C) J Leadbetter <j@jleadbetter.com>
Affero GPL v3
"""

from nicegui import ui
from nicegui.elements.label import Label

from frontend.widgets.base import BaseWidget


class OptionWidget(BaseWidget):
    def __init__(self, text: str, value: bool):
        self._text = text
        self._value = value

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

        with ui.grid(columns='auto auto auto auto'):
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

    def display(self):
        def save_settings():
            ui.notify('Work in progress')

        app_settings = self._adapters.get('AppSettingsDBPort').get_or_default()

        with ui.card().classes('absolute-center'):
            ui.label('Settings').classes('text-3xl')
            ui.separator()

            OptionWidget(
                'Can multiple people use the app?',
                app_settings.multiuser_mode,
            ).display()
            OptionWidget(
                'Log in without a password?',
                app_settings.passwordless_login,
            ).display()
            OptionWidget(
                'Show user list on the login page?',
                app_settings.show_users_on_login_screen,
            ).display()
            '''

            with ui.grid(columns='auto auto auto auto'):
                Op

                ui.label('Can multiple people use the app?').classes('border-solid! rounded-sm')
                no1 = ui.label('no').classes('inline-block align-text-bottom! outline text-right text-amber-600 px-4')
                switch1 = ui.switch(
                    value=app_settings.multiuser_mode,
                    on_change=lambda: ui.notify('changed'),
                )
                yes1 = ui.label('yes').classes('text-left text-green-600 px-4')

                ui.label('Log in without a password?')
                no2 = ui.label('no').classes('text-right text-amber-600')
                switch2 = ui.switch(value=app_settings.passwordless_login)
                yes2 = ui.label('yes').classes('text-left text-green-600')

                ui.label('Show user list on the login page?')
                no3 = ui.label('no').classes('text-right text-amber-600')
                switch3 = ui.switch(value=app_settings.show_users_on_login_screen)
                yes3 = ui.label('yes').classes('text-left text-green-600')

            ui.button('Save', on_click=save_settings).classes('self-center')

        update_no_and_yes(switch1.value, no1, yes1)
            '''
