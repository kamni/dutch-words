"""
Copyright (C) J Leadbetter <j@jleadbetter.com>
Affero GPL v3
"""

from nicegui import ui


def Header():
    """
    Header shared by all pages
    """

    with ui.header():
        ui.label('10,000 Words').classes('text-2xl')
