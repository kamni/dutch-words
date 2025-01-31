"""
Copyright (C) J Leadbetter <j@jleadbetter.com>
Affero GPL v3
"""

from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.widgets import Button


# To be replaced by screen content
class TempButton(Button):
    pass


class RegistrationModal(ModalScreen):
    """
    Register a new user
    """

    def compose(self) -> ComposeResult:
        yield TempButton("First Time", variant="primary")
