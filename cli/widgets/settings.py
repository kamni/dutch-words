"""
Copyright (C) J Leadbetter <j@jleadbetter.com>
Affero GPL v3
"""

from pathlib import Path

from textual.app import ComposeResult
from textual.containers import Center, Container, Horizontal
from textual.widgets import Button, Static, Switch


class SettingsWidget(Container):
    """
    Configure settings for the app
    """

    CSS_PATH = [
        (Path(__file__).resolve().parent / 'css' / 'settings.tcss').as_posix(),
    ]

    def on_switch_changed(self, event: Switch.Changed):
        switch = event.switch
        base = switch.id.rsplit('-', 1)[0]
        if switch.value:
            yes = self.query_one(f'#{base}-yes')
            yes.remove_class('settings-yes-unselected')
            yes.add_class('settings-yes-selected')

            no = self.query_one(f'#{base}-no')
            no.remove_class(f'settings-no-selected')
            no.add_class(f'settings-no-unselected')
        else:
            no = self.query_one(f'#{base}-no')
            no.remove_class('settings-no-unselected')
            no.add_class('settings-no-selected')

            yes = self.query_one(f'#{base}-yes')
            yes.remove_class(f'settings-yes-selected')
            yes.add_class(f'settings-yes-unselected')

    def compose(self) -> ComposeResult:
        yield Center(
            Center(
                Center(
                    Horizontal(
                        Static(
                            'Are multiple people using this app?',
                            classes='settings-question',
                        ),
                        Static(
                            'no',
                            id='multiuser-no',
                            classes='settings-no settings-no-selected',
                        ),
                        Switch(
                            value=False,
                            id='multiuser-switch',
                            classes='settings-switch',
                        ),
                        Static(
                            'yes',
                            id='multiuser-yes',
                            classes='settings-yes settings-yes-unselected',
                        ),
                        classes='settings-switch-wrapper',
                    ),
                ),
                Center(
                    Horizontal(
                        Static(
                            'Login without a password?',
                            classes='settings-question',
                        ),
                        Static(
                            'no',
                            id='passwordless-no',
                            classes='settings-no settings-no-unselected',
                        ),
                        Switch(
                            value=True,
                            id='passwordless-switch',
                            classes='settings-switch',
                        ),
                        Static(
                            'yes',
                            id='passwordless-yes',
                            classes='settings-yes settings-yes-selected',
                        ),
                        classes='settings-switch-wrapper',
                    ),
                ),
                Center(
                    Horizontal(
                        Static(
                            'Show usernames on login screen?',
                            classes='settings-question',
                        ),
                        Static(
                            'no',
                            id='show-usernames-no',
                            classes='settings-no settings-no-unselected',
                        ),
                        Switch(
                            value=True,
                            id='show-usernames-switch',
                            classes='settings-switch',
                        ),
                        Static(
                            'yes',
                            id='show-usernames-yes',
                            classes='settings-yes settings-yes-selected',
                        ),
                        classes='settings-switch-wrapper',
                    ),
                ),
                Center(
                    Button(
                        'Save Settings',
                        variant='primary',
                        id='settings-button',
                    ),
                    id='settings-button-wrapper',
                    classes='step-button',
                ),
                id='settings-text-wrapper',
            ),
        )

    def on_button_pressed(self, event: Button.Pressed):
        event.button.disabled = True

    def on_mount(self) -> None:
        self.query_one(Switch).focus()
