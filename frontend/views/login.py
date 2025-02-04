"""
Copyright (C) J Leadbetter <j@jleadbetter.com>
Affero GPL v3
"""

from fastapi.responses import RedirectResponse
from nicegui import ui

from frontend.views.base import BaseView


class LoginView(BaseView):
    """
    A combination login and signup view
    """

    def __init__(self):
        super().__init__()
        self._auth = self._adapters.get('AuthPort')

    def setup(self):
        if not self._app_settings.is_configured:
            self._redirect = '/configure'

        content = []
        self._page_content = content
