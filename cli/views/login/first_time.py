"""
Copyright (C) J Leadbetter <j@jleadbetter.com>
Affero GPL v3
"""

import os

from textual.app import ComposeResult
from textual.containers import Center, Container, Horizontal, VerticalGroup
from textual.screen import ModalScreen
from textual.widgets import Button, RadioButton, RadioSet, Static

from ...widgets.title import MainTitle


class Step1Text(Horizontal):
    def compose(self) -> ComposeResult:
        from textual.containers import HorizontalGroup
        yield Center(
            Center(
                Static('Welcome to 10,000 Words!', classes='step1-text'),
                Static("Configure the app to get started.", classes='step1-text'),
                Center(
                    Button('Get Started', variant='primary', id='step1-button'),
                    id='step1-button-wrapper',
                ),
                id='step1-text-wrapper',
            ),
        )


class Step1(Container):
    """
    Give a welcome message
    """

    def compose(self) -> ComposeResult:
        yield MainTitle(id='main-title')
        yield Step1Text(id='step1-text')


class FirstTimeModal(ModalScreen):
    """
    Configure the app for the first time and register a user
    """

    CSS_FILE = os.path.join('..', 'css', 'first_time.tcss')

    def compose(self) -> ComposeResult:
        yield Step1(id='step1')
