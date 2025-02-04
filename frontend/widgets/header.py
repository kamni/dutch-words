"""
Copyright (C) J Leadbetter <j@jleadbetter.com>
Affero GPL v3
"""

from frontend.widgets.base import BaseWidget

from nicegui import app, ui


class Header(BaseWidget):
    """
    Displays a header on the page
    """

    def display(self):
        def logout() -> None:
            app.storage.user.clear()
            ui.navigate.to('/')

        settings = self._adapters.get('AppSettingsDBPort').get()
        user = app.storage.user

        with ui.header():
            ui.label('10,000 Words').classes('text-2xl')
            ui.space()
            if user and user.get('authenticated', False):
                ui.icon('user')
                ui.label(user['display_name'])

                if settings and settings.show_logout:
                if settings and (
                    not settings.passwordless_login
                    and not settings.multiuser_mode
                ):
                    ui.button(on_click=logout, icon='logout').props('outline round')
