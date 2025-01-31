"""
Copyright (C) J Leadbetter <j@jleadbetter.com>
Affero GPL v3
"""

import os

from textual.app import ComposeResult
from textual.containers import Center, Container, Horizontal, Middle
from textual.reactive import reactive
from textual.screen import ModalScreen
from textual.widgets import Button, RadioButton, RadioSet, Static

from ...widgets.title import MainTitle


class FirstTimeModal(ModalScreen):
    """
    Configure the app for the first time and register a user
    """

    CSS_FILE = os.path.join('..', 'css', 'first_time.tcss')

    def compose(self) -> ComposeResult:
        self.steps = [
            Step1(id='step1'),
            Step2(id='step2'),
            Step3(id='step3'),
        ]
        yield Container(
            self.steps[0],
            id='first-time-wrapper',
        )

    def get_next_step(self):
        def _iterator():
            self.steps = [
                Step1(id='step1'),
                Step2(id='step2'),
                Step3(id='step3'),
            ]
            for step in self.steps:
                yield step
        return _iterator()

    def on_button_pressed(self, event: Button.Pressed):
        button = event.button
        current_step_idx = int(button.id.split('-')[0][-1])
        # TODO: run logic for step

        try:
            next_step_idx = int(button.name.split('-')[1])
            next_step = self.steps[next_step_idx - 1]
        except IndexError:
            # TODO: return back to login
            pass

        self.query('BaseStep').last().remove()
        self.query_one('#first-time-wrapper').mount(next_step)


class BaseStep(Container):
    """
    Base class for easy filtering
    """
    pass


class Step1(BaseStep):
    """
    Give a welcome message
    """

    def compose(self) -> ComposeResult:
        yield MainTitle(id='main-title')
        yield Step1Text(id='step1-text')


class Step1Text(Horizontal):
    def compose(self) -> ComposeResult:
        yield Center(
            Center(
                Static('Welcome to 10,000 Words!', classes='step1-text'),
                Static("Configure the app to get started.", classes='step1-text'),
                Center(
                    Button(
                        'Get Started',
                        variant='primary',
                        id='step1-button',
                        name='next-2',
                    ),
                    id='step1-button-wrapper',
                ),
                id='step1-text-wrapper',
            ),
        )


class Step2(BaseStep):
    """
    Configure the app
    """

    def compose(self) -> ComposeResult:
        # TODO: button for back, forward
        yield Static('Step 2')


class Step3(BaseStep):
    """
    Create the first user, who will be an admin
    """

    def compose(self) -> ComposeResult:
        # TODO: button for back, forward
        yield Static('Step3')
