"""
Copyright (C) J Leadbetter <j@jleadbetter.com>
Affero GPL v3
"""

from nicegui import app, ui

from frontend.views.base import BaseView
from frontend.widgets.configure import ConfigureWidget


class ConfigureView(BaseView):
    """
    Configure the app.

    This view has two modes.
    The first time the app is configured, no login is necessary.
    However, subsequent access requires an admin user.
    """

    def setup(self):
        if self._app_settings.is_configured:
            if not app.storage.user.get('authenticated', False):
                self._redirect = '/login'
                return False

        self._page_content.append(ConfigureWidget())
        return True

