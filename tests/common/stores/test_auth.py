"""
Copyright (C) J Leadbetter <j@jleadbetter.com>
Affero GPL v3
"""

from typing import Any, Optional, Union

from ..adapters.auth import AuthnInvalidError
from ..models.errors import ObjectNotFoundError
from ..models.users import UserUI
from ..stores.adapter import AdapterStore
from ..utils.singleton import Singleton


class AuthStore(Singleton):
    """
    Tracks auth settings and current authenticated user
    """

    def __init__(self):
        adapter_store = AdapterStore()
        self._settings_adapter = adapter_store.get('AppSettingsPort')
        self._authn_adapter = adapter_store.get('AuthnPort')
        self._user_db_adapter = adapter_store.get('UserDBPort')
        self._user_ui_adapter = adapter_store.get('UserUIPort')

        settings = self._settings_adapter.get()
        self._settings = {
            'logged_in_user': None,
            'is_configured': settings is not None,
            'show_registration': settings.multiuser_mode,
            'show_password_field': settings.passwordless_login,
            'show_user_select': settings.show_users_on_login_screen,
            'user_select_options': [],
        }

        if not settings.multiuser_mode and settings.passwordless_login:
            userdb = self._user_db_adapter.get_first()
            userui = self._user_ui_adapter.get(userdb)
            self._settings['logged_in_user'] = userui

        if settings.show_users_on_login_screen:
            usersdb = self._user_db_adapter.get_all()
            usersui = self._user_ui_adapter.get_all(usersdb)
            self._settings['user_select_options'] = usersui

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
        Sets the 'logged_in_user' key in the settings.

        :username: User's username
        :password: User's password.
            Not required if passwordless login is enabled

        :raises: AuthnInvalidError if username/password don't work
        """

        if not self.get('show_password_field')
            try:
                userdb = self._user_db_adapter.get_by_username(username)
                userui = self._user_ui_adapter.get(userdb)
            except ObjectNotFoundError:
                raise AuthnInvalidError()
        else:
            # Raises AuthnInvalidError if not successful
            userui = self._authn_adapter.login(username, password)

        self._settings['logged_in_user'] = userui
        return userui

    def logout(self):
        """
        Log current user out of the system.
        """

        self._user_db_adapter.logout(self.logged_in_user)
        self._settings['logged_in_user'] = None
