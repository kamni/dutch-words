"""
Copyright (C) J Leadbetter <j@jleadbetter.com>
Affero GPL v3
"""

from asgiref.sync import sync_to_async
from collections.abc import Callable
from typing import Any, List, Optional

from fastapi.responses import RedirectResponse
from nicegui import ui

from common.stores.adapter import AdapterStore
from common.stores.app import AppSettingsStore
from frontend.widgets.header import Header


class BaseView:
    """
    Base for all views in the app
    """

    def __init__(self):
        self._adapters = AdapterStore()
        self._app_settings = AppSettingsStore()

        self._page_content = []
        self._redirect = None
        self._next_url = None

    async def display(self) -> Any:
        """
        Show the content of the view.
        Redirect if setup determines user should be somewhere else.
        """

        Header().display()

        # Body
        self.setup()
        if self._redirect:
            return RedirectResponse(self._redirect)

        for content in self._page_content:
            content.display()

        ui.on('done', self.navigate_next)
        ui.on('cancel', ui.navigate.back)

    def navigate_next(self):
        """
        When a user is done, navigate to the next logical url.
        """
        if self._next_url:
            ui.navigate.to(self._next_url)
        else:
            ui.navigate.back

    def setup(self):
        """
        Set the widgets or other content to be displayed.
        All content must implement a `display` function.
        """
        pass
