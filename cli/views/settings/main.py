"""
Copyright (C) J Leadbetter <j@jleadbetter.com>
Affero GPL v3
"""

import os
from typing import Dict

from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.screen import Screen
from textual.widgets import Button, Footer, Label, Static, Switch, Tabs, Tab

from common.stores.adapter import AdapterStore


# TODO: To be replaced by screen content
class TempButton(Button):
    pass


class SettingsScreen(Screen):
    """
    Manage the settings for the app
    """

    CSS_PATH = os.path.join('..', 'css', 'app_settings.tcss')

    BINDINGS = [
        ('s', 'save', 'Save'),
        ('escape', 'cancel', 'Cancel'),
    ]

    _TAB_CONFIG = {
        'switches': [
            ('Multiple users?', 'multiuser-switch'),
            ('Automatic login?', 'automatic-login-switch'),
            ('Show users on login screen?', 'show-users-switch'),
        ],
        'tabs': [
            {
                'id': 'desktop-tab',
                'name': 'Desktop User',
                'description_text': 'Single-user, login not required  (recommended)',
                'default_values': {
                    'multiuser-switch': False,
                    'automatic-login-switch': True,
                    'show-users-switch': False,
                },
                'configurable': False,
            },
            {
                'id': 'webserver-tab',
                'name': 'Web Server',
                'description_text': 'Multi-user, login always required',
                'default_values': {
                    'multiuser-switch': True,
                    'automatic-login-switch': False,
                    'show-users-switch': False,
                },
                'configurable': False,
            },
            {
                'id': 'paranoid-tab',
                'name': 'Paranoid',
                'description_text': 'Single-user, login always required',
                'default_values': {
                    'multiuser-switch': False,
                    'automatic-login-switch': False,
                    'show-users-switch': False,
                },
                'configurable': False,
            },
            {
                'id': 'trusting-tab',
                'name': 'Trusting',
                'description_text': 'Multiuser, no login required',
                'default_values': {
                    'multiuser-switch': True,
                    'automatic-login-switch': True,
                    'show-users-switch': True,
                },
                'configurable': False,
            },
            {
                'id': 'custom-tab',
                'name': 'Custom',
                'description_text': 'Custom configuration (advanced)',
                'default_values': {
                    'multiuser-switch': False,
                    'automatic-login-switch': False,
                    'show-users-switch': False,
                },
                'configurable': True,
            },
        ],
    }

    @property
    def settings_adapter(self):
        if not hasattr(self, '_settings_adapter') or self._app_settings is None:
            adapters = AdapterStore()
            self._settings_adapter = adapters.get('AppSettingsPort')
        return self._settings_adapter

    @property
    def settings(self):
        if not hasattr(self, '_settings'):
            self._settings = self.settings_adapter.get()
        return self._settings

    def action_cancel(self):
        # Go to registration if not user
        # Go to previous mode otherwise?
        # TODO: implement
        pass

    def action_save(self):
        # TODO: implement
        pass

    def compose(self) -> ComposeResult:
        if not self.settings:
            yield Static('Welcome to 10,000 Words!')
            yield Static(
                'Before we get started, '
                'please tell us how you want to use the app.'
            )

        yield Static('Please choose your configuration:')

        yield Tabs(*[
            Tab(tab['name'], id=tab['id'])
            for tab in self._TAB_CONFIG['tabs']
        ])

        yield Static('', id='description-text')

        for text, id in self._TAB_CONFIG['switches']:
            yield Horizontal(
                Static(text, classes='label'),
                Switch(value=False, animate=False, disabled=True, id=id),
                classes='container',
            )

        yield TempButton("Configure", variant="primary")
        yield Footer()

    def on_tabs_tab_activated(self, event: Tabs.TabActivated) -> None:
        tab_id = event.tab.id
        tab = list(filter(
            lambda x: x['id'] == tab_id,
            self._TAB_CONFIG['tabs'],
        ))[0]
        self.query_one('#description-text').update(tab['description_text'])

        for _, switch_id in self._TAB_CONFIG['switches']:
            switch = self.query_one(f'#{switch_id}')
            switch.value = tab['default_values'][switch.id]
            switch.disabled = not tab['configurable']

    def on_mount(self):
        self.query_one(f'#desktop-tab').focus()
