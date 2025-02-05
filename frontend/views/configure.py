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
        self._next_url = '/register'
        '''
        if self._app_settings.is_configured:
            if not app.storage.user.get('authenticated', False):
                self._redirect = redirect
                return False
            else:
                redirect = app.storage.user.get('referrer_path', '/')
        else:
            redirect = '/registration'
        '''
        self._page_content.append(ConfigureWidget())
        return True

