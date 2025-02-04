"""
Copyright (C) J Leadbetter <j@jleadbetter.com>
Affero GPL v3
"""

from collections.abc import Callable
from typing import Any, List, Optional

from common.stores.adapter import AdapterStore
from frontend.widgets.header import Header


class BaseView:
    """
    Base for all views in the app
    """

    def __init__(self):
        self._adapters = AdapterStore()

        self._page_content = []
        self.set_content()

    def display(self) -> Any:
        """
        Show the content of the view
        """

        Header().display()
        for content in self._page_content:
            content.display()

    def set_content(self):
        """
        Set the widgets or other content to be displayed.
        All content must implement a `display` function.
        """
        pass
