"""
Copyright (C) J Leadbetter <j@jleadbetter.com>
Affero GPL v3
"""

from collections.abc import Callable
from typing import List, Optional

from frontend.widgets.base import Header


def PageBase(page_content: Optional[List[Callable]] = None):
    """
    Base for all pages
    """

    page_content = page_content or []

    Header()
    for content in page_content:
        content()
