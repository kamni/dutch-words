"""
Copyright (C) J Leadbetter <j@jleadbetter.com>
Affero GPL v3
"""

from django.test import TestCase

from common.stores.adapter import AdapterStore
from common.stores.auth import AuthStore
from common.stores.settings import SettingsStore
from common.utils.singleton import Singleton


class TestAuthStore(TestCase):
    """
    Tests for common.stores.auth.AuthStore
    """

    @classmethod
    def setUpClass(cls):
        # Get rid of lurking instances before starting tests
        Singleton.destroy(AdapterStore)
        Singleton.destroy(AuthStore)
        Singleton.destroy(SettingsStore)

        adapter_store = AdapterStore(subsection='dev.django')
        cls.store = AuthStore()
        super().setUpClass()

    def tearDown(self):
        Singleton.destroy(AuthStore)

    def test_is_singleton(self):
        pass

    def test_init_settings_does_not_exist(self):
        
        pass

    def test_init_settings_false_false_false(self):
        """
        multiuser_mode = False
        paswordless_login = False
        show_users_on_login_screen = False
        """
        pass

    '''
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
    '''

    def test_init_settings_true_false_false(self):
        """
        multiuser_mode = True
        passwordless_login = False
        show_users_on_login_screen = False
        """
        pass

    def test_init_settings_true_true_false(self):
        """
        multiuser_mode = True
        passwordless_login = True
        show_users_on_login_screen = False
        """
        pass

    def test_init_settings_true_true_true(self):
        """
        multiuser_mode = True
        passwordless_login = True
        show_users_on_login_screen = True
        """
        pass

    def test_init_settings_false_true_false(self):
        """
        mutliuser_mode = False
        passwordless_login = True
        show_users_on_login_screen = False
        """
        pass

    def test_init_settings_false_true_true(self):
        """
        multiuser_mode = False
        passwordless_login = True
        show_users_on_login_screen = True
        """
        pass

    def test_init_settings_false_false_true(self):
        """
        multiuser_mode = False
        passwordless_login = False
        show_users_on_login_screen = True
        """
        pass

    def test_login(self):
        pass

    def test_login_user_does_not_exist(self):
        pass

    def test_login_user_has_no_password(self):
        pass

    def test_login_passwordless_login(self):
        pass

    def test_login_passwordless_login_user_does_not_exist(self):
        pass

    def test_get_setting_does_not_exist(self):
        pass

    def test_logout(self):
        pass

    def test_logout_user_not_logged_in(self):
        pass
