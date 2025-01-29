"""
Copyright (C) J Leadbetter <j@jleadbetter.com>
Affero GPL v3
"""

from typing import Any, Optional, Union

from ..ports.auth import AuthnInvalidError
from ..models.errors import ObjectNotFoundError
from ..models.users import UserUI
from ..ports.auth import AuthnInvalidError
from ..stores.adapter import AdapterStore
from ..utils.singleton import Singleton


class AuthStore(Singleton):
    """
    Tracks auth settings and current authenticated user
    """

    LOGGED_IN_USER = 'logged_in_user'
    IS_CONFIGURED = 'is_configured'
    SHOW_REGISTRATION = 'show_registration'
    SHOW_PASSWORD_FIELD = 'show_password_field'
    SHOW_USER_SELECT = 'show_user_select'
    USER_SELECT_OPTIONS = 'user_select_options'

    def __init__(self):
        adapter_store = AdapterStore()
        self._settings_adapter = adapter_store.get('AppSettingsPort')
        self._authn_adapter = adapter_store.get('AuthnPort')
        self._user_db_adapter = adapter_store.get('UserDBPort')
        self._user_ui_adapter = adapter_store.get('UserUIPort')

        settings = self._settings_adapter.get()
        self._settings = {
            LOGGED_IN_USER: None,
            IS_CONFIGURED: settings is not None,
            SHOW_REGISTRATION: settings.multiuser_mode,
            SHOW_PASSWORD_FIELD: settings.passwordless_login,
            SHOW_USER_SELECT: settings.show_users_on_login_screen,
            USER_SELECT_OPTIONS: [],
        }

        if not settings.multiuser_mode and settings.passwordless_login:
            userdb = self._user_db_adapter.get_first()
            userui = self._user_ui_adapter.get(userdb)
            self._settings[LOGGED_IN_USER] = userui

        if settings.show_users_on_login_screen:
            usersdb = self._user_db_adapter.get_all()
            usersui = self._user_ui_adapter.get_all(usersdb)

            if not settings.multiuser_mode and len(usersui) > 1:
                usersui = usersui[0]

            self._settings[USER_SELECT_OPTIONS] = usersui

    def get(self, setting: str) -> Union[Any, None]:
        """
        Get specified setting.

        Available settings:

        * logged_in_user
        * is_configured
        * show_registration
        * show_password_field
        * show_user_select
        * user_select_options

        :setting: One of the available settings

        :return: Specified setting, if exists; otherwise None
        """

        setting = self._settings.get(setting)
        return setting

    def login(self, username: str, password: Optional[str]=None) -> UserUI:
        """
        Log in the user.
        Sets the LOGGED_IN_USER key in the settings.

        :username: User's username
        :password: User's password.
            Not required if passwordless login is enabled

        :raises: AuthnInvalidError if username/password don't work
        """

        if not self.get(SHOW_PASSWORD_FIELD)
            try:
                userdb = self._user_db_adapter.get_by_username(username)
                userui = self._user_ui_adapter.get(userdb)
            except ObjectNotFoundError:
                # This message is only for internal logging.
                # Do not show this to users,
                # as it could facilitate brute-forcing usernames.
                raise AuthnInvalidError(f'User {username} not found')
        else:
            # Raises AuthnInvalidError if not successful
            userui = self._authn_adapter.login(username, password)

        self._settings[LOGGED_IN_USER] = userui
        return userui

    def logout(self):
        """
        Log current user out of the system.
        """

        self._user_db_adapter.logout(self.logged_in_user)
        self._settings[LOGGED_IN_USER] = None
