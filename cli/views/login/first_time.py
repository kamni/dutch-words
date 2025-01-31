"""
Copyright (C) J Leadbetter <j@jleadbetter.com>
Affero GPL v3
"""

from pathlib import Path

from textual.app import ComposeResult
from textual.containers import Center, Container, Horizontal, Middle
from textual.screen import ModalScreen
from textual.widgets import Button, Static, Switch

from common.stores.adapter import AdapterStore

from ...widgets.registration import RegistrationWidget
from ...widgets.settings import SettingsWidget
from ...widgets.title import MainTitleWidget

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

    CSS_PATH = [
        (Path(__file__).resolve().parent / 'css' / 'first_time.tcss').as_posix(),
    ] + MainTitleWidget.CSS_PATH + SettingsWidget.CSS_PATH + \
        RegistrationWidget.CSS_PATH

    @property
    def userdb_adapter(self):
        if not hasattr(self, '_userdb_adapter') or self._userdb_adapter is None:
            adapters = AdapterStore()
            self._userdb_adapter = adapters.get('UserDBPort')
        return self._userdb_adapter

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

        try:
            current_step_idx = int(button.id.split('-')[0][-1])
            current_step = self.steps[current_step_idx - 1]
            current_step.handle_it()

            next_step_idx = int(button.name.split('-')[1])
            next_step = self.steps[next_step_idx - 1]
        except IndexError:
            self.app.pop_screen()
            return

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
        yield MainTitleWidget(id='main-title')
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


class Step2(BaseStep, SettingsWidget):
    """
    Configure the app
    """

    def on_mount(self):
        super().mount()

        # In order to go to the next step
        # we need to update the button from the original widget.
        # The `name` and `id` fields are not reactive,
        # So we need to add a new one.
        button = self.query_one('#settings-button')
        new_button = Button(
            button.label,
            variant=button.variant,
            id='step2-button',
            name='next-3',
        )
        container = self.query_one('#settings-button-wrapper')
        button.remove()
        container.mount(new_button)


class Step3(BaseStep, RegistrationWidget):
    """
    Create the first user, who will be an admin
    """

    def on_mount(self):
        super().mount()

        # In order to finish setup/registration
        # we need to update the button from the original widget.
        # The `name` and `id` fields are not reactive,
        # So we need to add a new onw
        button = self.query_one('#registration-button')
        new_button = Button(
            button.label,
            variant=button.variant,
            id='step3-button',
            name='next-4',
        )
        container = self.query_one('#registration-button-wrapper')
        button.remove()
        container.mount(new_button)

    def handle_it(self):
        # The first user should be an admin
        user = self.userdb_adapter.get_first()
        if not user.is_admin:
            user.is_admin = True
        self.userdb_adapter.update(user)
