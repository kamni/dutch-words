"""
Copyright (C) J Leadbetter <j@jleadbetter.com>
Affero GPL v3
"""

from abc import ABC, abstractmethod

from common.stores.adapter import AdapterStore


class BaseWidget(ABC):
    """
    Base for reusable page components

    Implement a `display` method.
    """

    def __init__(self):
        self._adapters = AdapterStore()

    @abstractmethod
    def display(self):
        """
        Display the content of the widget.
        """

        pass
