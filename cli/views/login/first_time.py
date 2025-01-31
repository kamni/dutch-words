"""
Copyright (C) J Leadbetter <j@jleadbetter.com>
Affero GPL v3
"""

import os

from textual.app import ComposeResult
from textual.containers import Center, Container, Horizontal, Middle
from textual.screen import ModalScreen
from textual.widgets import Button, RadioButton, RadioSet, Static

from common.stores.adapter import AdapterStore

from ...widgets.title import MainTitle


class FirstTimeModal(ModalScreen):
    """
    Configure the app for the first time and register a user
    """

    CSS_FILE = os.path.join('..', 'css', 'first_time.tcss')

    @property
    def settings(self):
        if not hasattr(self, '_settings') or self._settings is None:
            adapters = AdapterStore()
            self._settings = adapters.get('AppSettingsPort')
        return self._settings

    @property
    def user_db(self):
        if not hasattr(self, '_user_db') or self._user_db is None:
            adapters = AdapterStore()
            self._user_db = adapters.get('UserDBPort')
        return self._user_db

    @property
    def user_ui(self):
        if not hasattr(self, '_user_ui') or self._user_ui is None:
            adapters = AdapterStore()
            self._user_ui = adapters.get('UserUIPort')
        return self._user_ui

    def compose(self) -> ComposeResult:
        self.steps = [
            Step1(id='step1'),
            Step2(id='step2'),
            Step3(id='step3'),
        ]
        yield Middle(
            self.steps[0],
            id='first-time-wrapper',
        )

    def on_button_pressed(self, event: Button.Pressed):
        button = event.button

        current_step_idx = int(button.id.split('-')[0][-1])
        current_step = self.steps[current_step_idx - 1]
        current_step.handle_it()
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

    def handle_it(self):
        pass


class Step1(BaseStep):
    """
    Give a welcome message
    """

    def compose(self) -> ComposeResult:
        yield MainTitle(id='main-title')
        yield Horizontal(
            Center(
                Center(
                    Static('Welcome to 10,000 Words!', classes='step-text'),
                    Static("Configure the app to get started.", classes='step-text'),
                    Center(
                        Button(
                            'Get Started',
                            variant='primary',
                            id='step1-button',
                            name='next-2',
                        ),
                        id='step1-button-wrapper',
                        classes='step-button',
                    ),
                    id='step1-text-wrapper',
                ),
            ),
            id='step1-text',
        )

    def handle_it(self, **kwargs):
        # Nothing to do on the welcome screen
        pass


class Step1Text(Horizontal):
    def compose(self) -> ComposeResult:
        yield Center(
            Center(
                Static('Welcome to 10,000 Words!', classes='step-text'),
                Static("Configure the app to get started.", classes='step-text'),
                Center(
                    Button(
                        'Get Started',
                        variant='primary',
                        id='step1-button',
                        name='next-2',
                    ),
                    id='step1-button-wrapper',
                    classes='step-button',
                ),
                id='step1-text-wrapper',
            ),
        )


class Step2(BaseStep):
    """
    Configure the app
    """

    def compose(self) -> ComposeResult:
        yield Center(
            Center(
                Center(
                    Button(
                        'Save Settings',
                        variant='primary',
                        id='step2-button',
                        name='next-3',
                    ),
                    id='step2-button-wrapper',
                    classes='step-button',
                ),
                id='step2-text-wrapper',
            ),
        )


class Step3(BaseStep):
    """
    Create the first user, who will be an admin
    """

    def compose(self) -> ComposeResult:
        # TODO: button for back, forward
        yield Static('Step3')
