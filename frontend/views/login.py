"""
Copyright (C) J Leadbetter <j@jleadbetter.com>
Affero GPL v3
"""

from fastapi.responses import RedirectResponse
from nicegui import UI

from frontend.views.base import BaseView


class LoginView(BaseView):
    """
    A combination login and signup view
    """

    def display(self):
        pass
