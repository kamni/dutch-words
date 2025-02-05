"""
Copyright (C) J Leadbetter <j@jleadbetter.com>
Affero GPL v3
"""

import string
from collections.abc import Callable
from functools import partial
from typing import List, Optional

from nicegui import ui

from frontend.widgets.base import BaseWidget


class ValidationError(Exception):
    """
    Thrown when an input fails to validate
    """
    pass


class ValidatingInput(BaseWidget):
    """
    Input that runs validation on the content.
    """

    def __init__(self, title: str, validators: Optional[List[Callable]]=None):
        self._title = title
        self._validators = validators or []

        self._input = None
        self._error = None

    def display(self):
        self._input = ui.input(self._title).classes('self-center')
        self._error = ui.label('').classes('text-amber-600 self-center height-fit hidden')

    def validate(self):
        # Reset the validation errors
        self._error.classes(add='hidden')
        self._error.text = ''

        value = self._input.value
        errors = []
        for validate in self._validators:
            try:
                validate(value)
            except ValidationError as exc:
                errors.append(str(exc))

        if errors:
            error_msg = ' '.join([
                f'{self._title} {msg}' for msg in errors
            ])
            self._error.text = error_msg
            self._error.classes(remove='hidden')
            return False

        return True


class RegistrationWidget(BaseWidget):
    """
    Provides a registration form for a new user.
    """

    def display(self):
        def text_is_x_characters_long(text: str, expected_length: int):
            if not len(text.strip()) > expected_length - 1:
                raise ValidationError(
                    f'must be at least {expected_length} characters long.',
                )

        def text_does_not_contain_spaces(text: str):
            text = text.strip()
            if any([char in text for char in string.whitespace]):
                raise ValidationError('cannot contain spaces.')

        self._display_name = ValidatingInput('Name (Optional)')
        self._username = ValidatingInput(
            'Username',
            [
                partial(text_is_x_characters_long, expected_length=4),
                text_does_not_contain_spaces,
            ],
        )
        self._password = None
        if self._app_settings.show_password_field:
            self._password = ValidatingInput(
                'Password',
                [
                    partial(text_is_x_characters_long, expected_length=12),
                    text_does_not_contain_spaces,
                ],
            )

        def is_valid() -> bool:
            return all([
                self._display_name.validate(),
                self._username.validate(),
                self._password.validate() if self._password else True,
            ])

        def save_user():
            if not is_valid():
                return

            # TODO: actually save the user
            # TODO: admin?
            # TODO: auto-login?
            ui.notify(f'Welcome!')
            time.sleep(2)
            #self.emit_done()

        with ui.card().classes('absolute-center'):
            ui.label('Register for 10,000 Words').classes('text-3xl')
            ui.separator()

            self._display_name.display()
            self._username.display()
            if self._password:
                self._password.display()

            ui.separator()
            ui.button('Join', on_click=save_user).classes('self-center')


