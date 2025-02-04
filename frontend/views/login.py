"""
Copyright (C) J Leadbetter <j@jleadbetter.com>
Affero GPL v3
"""

from fastapi.responses import RedirectResponse
from nicegui import UI

from common.stores.adapter import AdapterStore
from common.stores.auth import AuthStore
from frontend.views.base import BaseView


class LoginView(BaseView):
    """
    A combination login and signup view
    """

    def set_page_content(self):
        if not self._auth.logged_in_use
        pass
