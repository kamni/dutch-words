"""
Copyright (C) J Leadbetter <j@jleadbetter.com>
Affero GPL v3
"""

import os

from textual.app import ComposeResult
from textual.containers import Center, Container, Horizontal, Middle
from textual.screen import ModalScreen
from textual.widgets import Button, Static, Switch

from common.stores.adapter import AdapterStore

from ...widgets.title import MainTitle

import logging
from textual.logging import TextualHandler

logging.basicConfig(
    level="NOTSET",
    handlers=[TextualHandler()],
)

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


class Step2(BaseStep):
    """
    Configure the app
    """

    def on_switch_changed(self, event: Switch.Changed):
        switch = event.switch
        base = switch.id.rsplit('-', 1)[0]
        if switch.value:
            yes = self.query_one(f'#{base}-yes')
            yes.remove_class('step2-yes-unselected')
            yes.add_class('step2-yes-selected')

            no = self.query_one(f'#{base}-no')
            no.remove_class(f'step2-no-selected')
            no.add_class(f'step2-no-unselected')
        else:
            no = self.query_one(f'#{base}-no')
            no.remove_class('step2-no-unselected')
            no.add_class('step2-no-selected')

            yes = self.query_one(f'#{base}-yes')
            yes.remove_class(f'step2-yes-selected')
            yes.add_class(f'step2-yes-unselected')

    def compose(self) -> ComposeResult:
        yield Center(
            Center(
                Center(
                    Horizontal(
                        Static(
                            'Are multiple people using this app?',
                            classes='step2-question',
                        ),
                        Static(
                            'no',
                            id='multiuser-no',
                            classes='step2-no step2-no-selected',
                        ),
                        Switch(
                            value=False,
                            id='multiuser-switch',
                            classes='step2-switch',
                        ),
                        Static(
                            'yes',
                            id='multiuser-yes',
                            classes='step2-yes step2-yes-unselected',
                        ),
                        classes='step2-switch-wrapper',
                    ),
                ),
                Center(
                    Horizontal(
                        Static(
                            'Login without a password?',
                            classes='step2-question',
                        ),
                        Static(
                            'no',
                            id='passwordless-no',
                            classes='step2-no step2-no-unselected',
                        ),
                        Switch(
                            value=True,
                            id='passwordless-switch',
                            classes='step2-switch',
                        ),
                        Static(
                            'yes',
                            id='passwordless-yes',
                            classes='step2-yes step2-yes-selected',
                        ),
                        classes='step2-switch-wrapper',
                    ),
                ),
                Center(
                    Horizontal(
                        Static(
                            'Show usernames on login screen?',
                            classes='step2-question',
                        ),
                        Static(
                            'no',
                            id='show-usernames-no',
                            classes='step2-no step2-no-unselected',
                        ),
                        Switch(
                            value=True,
                            id='show-usernames-switch',
                            classes='step2-switch',
                        ),
                        Static(
                            'yes',
                            id='show-usernames-yes',
                            classes='step2-yes step2-yes-selected',
                        ),
                        classes='step2-switch-wrapper',
                    ),
                ),
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

    def on_mount(self) -> None:
        self.query_one(Switch).focus()


class Step3(BaseStep):
    """
    Create the first user, who will be an admin
    """

    def compose(self) -> ComposeResult:
        # TODO: button for back, forward
        yield Static('Step3')
