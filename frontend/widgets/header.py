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

    @property
    def show_logout(self):
        return self._app_settings.show_logout

    def display(self):
        def logout() -> None:
            app.storage.user.clear()
            ui.navigate.to('/')

        user = app.storage.user
        user_authenticated = user.get('authenticated', False)
        show_logout = self.show_logout

        with ui.header():
            ui.label('💬').classes('text-2xl')
            ui.label('10,000 Words').classes('text-2xl')
            ui.space()
            if user_authenticated:
                ui.icon('user').classes('text-2xl')
                ui.label(user['display_name']).classes('text-2xl')

                if show_logout:
                    ui.button(
                        on_click=logout,
                        icon='logout',
                    ).props('outline round')

