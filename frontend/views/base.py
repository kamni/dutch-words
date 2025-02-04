"""
Copyright (C) J Leadbetter <j@jleadbetter.com>
Affero GPL v3
"""

from asgiref.sync import sync_to_async
from collections.abc import Callable
from typing import Any, List, Optional

from fastapi.responses import RedirectResponse

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

    async def display(self) -> Any:
        """
        Show the content of the view
        """

        Header().display()

        # Body
        self.set_content()
        for content in self._page_content:
            content.display()

        return self.return_next()

    def set_content(self):
        """
        Set the widgets or other content to be displayed.
        All content must implement a `display` function.
        """
        pass

    def return_next(self) -> Optional[RedirectResponse]:
        """
        If needed, return a redirect to the next view.
        """
        if self._redirect:
            return RedirectResponse(self._redirect)
