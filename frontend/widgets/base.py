"""
Copyright (C) J Leadbetter <j@jleadbetter.com>
Affero GPL v3
"""

from abc import ABC, abstractmethod

from common.stores.adapter import AdapterStore
from common.stores.app import AppSettingsStore


class BaseWidget(ABC):
    """
    Base for reusable page components

    Implement a `display` method.
    """

    def __init__(self):
        self._adapters = AdapterStore()
        self._app_settings = AppSettingsStore()

    @abstractmethod
    def display(self):
        """
        Display the content of the widget.
        """
        pass
