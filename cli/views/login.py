"""
Copyright (C) J Leadbetter <j@jleadbetter.com>
Affero GPL v3
"""

import logging

from textual.app import ComposeResult
from textual.containers import Center, Container, VerticalGroup
from textual.logging import TextualHandler
from textual.reactive import reactive
from textual.screen import Screen
from textual.widgets import Button, Footer, Input, Label, Static


logging.basicConfig(
    level=logging.DEBUG,
    handlers=[TextualHandler()],
)


TITLE_TEXT1 = """
   _   __        __     __     __
 /' )/' _`\    /' _`\ /' _`\ /' _`\\
(_, || ( ) |   | ( ) || ( ) || ( ) |
  | || | | |   | | | || | | || | | |
  | || (_) | _ | (_) || (_) || (_) |
  (_)`\___/'( )`\___/'`\___/'`\___/'
            |/
"""

TITLE_TEXT2 = """
  _       _                 _
 ( )  _  ( )               ( )
 | | ( ) | |   _    _ __  _| | ___
 | | | | | | /'_`\ ( '__)'_` /',__)
 | (_/ \_) |( (_) )| | ( (_| \__, \\
 `\___x___/'`\___/'(_) `\__,_|____/
"""

SUBTITLE_TEXT = 'Teach yourself 10,000+ words in another language'



class LoginScreen(Screen):
    CSS_PATH = 'login.tcss'

    def compose(self) -> ComposeResult:
        yield Container(
            Center(
                VerticalGroup(
                    Static(TITLE_TEXT1, classes='title-text'),
                    Static(TITLE_TEXT2, classes='title-text'),
                    id='title',
                ),
                id='title-wrapper',
            ),
            Center(
                Static(SUBTITLE_TEXT, classes='subtitle-text'),
                id='subtitle-wrapper',
            ),
            Center(
                VerticalGroup(
                    Input(placeholder='Username', id='username-input'),
                    Input(placeholder='Password', password=True, id='password-input'),
                    id='login',
                ),
                id='login-wrapper',
            ),
            Center(
                Button('Log In', variant='primary', id='login-button'),
                id='login-button-wrapper',
            ),
            id='wrapper'
        )
        yield Footer()

    def action_submit_form(self):
        button = self.query_one('#login-button')
        button.disabled = True

        username_field = self.query_one('#username-input')
        password_field = self.query_one('#password-input')

        from time import sleep
        sleep(5)
        button.remove_class('login-disabled')

        # TODO: remove/uninstall login screen; move to next one

    def on_button_pressed(self, event: Button.Pressed):
        self.action_submit_form()
