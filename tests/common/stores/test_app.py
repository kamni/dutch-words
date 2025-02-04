"""
Copyright (C) J Leadbetter <j@jleadbetter.com>
Affero GPL v3
"""

from django.test import TestCase

from app.models.app import AppSettings
from common.adapters.django_orm.auth import AuthInvalidError
from common.adapters.django_orm.users import UserDBDjangoORMAdapter
from common.adapters.ui.users import UserUIAdapter
from common.stores.adapter import AdapterStore
from common.stores.app import AppSettingsStore
from common.stores.config import ConfigStore
from common.utils.singleton import Singleton

from ...utils.users import make_user_db, make_user_ui


class TestAppSettingsStore(TestCase):
    """
    Tests for common.stores.auth.AppSettingsStore
    """

    @classmethod
    def setUpClass(cls):
        # Get rid of lurking instances before starting tests
        Singleton.destroy(AdapterStore)
        Singleton.destroy(AppSettingsStore)
        Singleton.destroy(ConfigStore)

        adapter_store = AdapterStore(subsection='dev.django')
        super().setUpClass()

    def tearDown(self):
        Singleton.destroy(AppSettingsStore)

    def test_is_singleton(self):
        auth_store1 = AppSettingsStore()
        self.assertFalse(auth_store1.get(AppSettingsStore.IS_CONFIGURED))

        AppSettings.objects.create(
            multiuser_mode=True,
            passwordless_login=True,
            show_users_on_login_screen=True,
        )
        auth_store2 = AppSettingsStore()
        self.assertFalse(auth_store2.get(AppSettingsStore.IS_CONFIGURED))

    def test_initialize_already_initialized(self):
        AppSettings.objects.create(
            multiuser_mode=True,
            passwordless_login=True,
            show_users_on_login_screen=True,
        )

        auth_store = AppSettingsStore()
        self.assertTrue(auth_store.get(AppSettingsStore.IS_CONFIGURED))

        AppSettings.objects.all().delete()
        auth_store.initialize()
        self.assertTrue(auth_store.get(AppSettingsStore.IS_CONFIGURED))

    def test_initialize_forced(self):
        AppSettings.objects.create(
            multiuser_mode=True,
            passwordless_login=True,
            show_users_on_login_screen=True,
        )

        auth_store = AppSettingsStore()
        self.assertTrue(auth_store.get(AppSettingsStore.IS_CONFIGURED))

        AppSettings.objects.all().delete()
        auth_store.initialize(force=True)
        self.assertFalse(auth_store.get(AppSettingsStore.IS_CONFIGURED))

    def test_init_settings_does_not_exist(self):
        usersdb = [
            UserDBDjangoORMAdapter().create(make_user_db())
            for i in range(3)
        ]
        usersui = UserUIAdapter().get_all(usersdb)

        auth_store = AppSettingsStore()
        expected = {
            AppSettingsStore.LOGGED_IN_USER: None,
            AppSettingsStore.IS_CONFIGURED: False,
            AppSettingsStore.USER_SELECT_OPTIONS: [],
            AppSettingsStore.SHOW_REGISTRATION: False,
            AppSettingsStore.SHOW_PASSWORD_FIELD: False,
            AppSettingsStore.SHOW_USER_SELECT: False,
        }
        returned = auth_store._settings
        self.assertEqual(expected, returned)

    def test_init_settings_false_false_false(self):
        """
        multiuser_mode = False
        passwordless_login = False
        show_users_on_login_screen = False
        """

        usersdb = [
            UserDBDjangoORMAdapter().create(make_user_db())
            for i in range(3)
        ]
        usersui = UserUIAdapter().get_all(usersdb)

        AppSettings.objects.create(
            multiuser_mode=False,
            passwordless_login=False,
            show_users_on_login_screen=False,
        )
        auth_store = AppSettingsStore()

        expected = {
            AppSettingsStore.LOGGED_IN_USER: None,
            AppSettingsStore.IS_CONFIGURED: True,
            AppSettingsStore.USER_SELECT_OPTIONS: [],
            AppSettingsStore.SHOW_REGISTRATION: False,
            AppSettingsStore.SHOW_PASSWORD_FIELD: True,
            AppSettingsStore.SHOW_USER_SELECT: False,
        }
        returned = auth_store._settings
        self.assertEqual(expected, returned)

    def test_init_settings_true_false_false(self):
        """
        multiuser_mode = True
        passwordless_login = False
        show_users_on_login_screen = False
        """

        usersdb = [
            UserDBDjangoORMAdapter().create(make_user_db())
            for i in range(3)
        ]
        usersui = UserUIAdapter().get_all(usersdb)

        AppSettings.objects.create(
            multiuser_mode=True,
            passwordless_login=False,
            show_users_on_login_screen=False,
        )
        auth_store = AppSettingsStore()

        expected = {
            AppSettingsStore.LOGGED_IN_USER: None,
            AppSettingsStore.IS_CONFIGURED: True,
            AppSettingsStore.USER_SELECT_OPTIONS: [],
            AppSettingsStore.SHOW_REGISTRATION: True,
            AppSettingsStore.SHOW_PASSWORD_FIELD: True,
            AppSettingsStore.SHOW_USER_SELECT: False,
        }
        returned = auth_store._settings
        self.assertEqual(expected, returned)

    def test_init_settings_true_true_false(self):
        """
        multiuser_mode = True
        passwordless_login = True
        show_users_on_login_screen = False
        """

        usersdb = [
            UserDBDjangoORMAdapter().create(make_user_db())
            for i in range(3)
        ]
        usersui = UserUIAdapter().get_all(usersdb)

        AppSettings.objects.create(
            multiuser_mode=True,
            passwordless_login=True,
            show_users_on_login_screen=False,
        )
        auth_store = AppSettingsStore()

        expected = {
            AppSettingsStore.LOGGED_IN_USER: None,
            AppSettingsStore.IS_CONFIGURED: True,
            AppSettingsStore.USER_SELECT_OPTIONS: [],
            AppSettingsStore.SHOW_REGISTRATION: True,
            AppSettingsStore.SHOW_PASSWORD_FIELD: False,
            AppSettingsStore.SHOW_USER_SELECT: False,
        }
        returned = auth_store._settings
        self.assertEqual(expected, returned)

    def test_init_settings_true_true_true(self):
        """
        multiuser_mode = True
        passwordless_login = True
        show_users_on_login_screen = True
        """

        usersdb = [
            UserDBDjangoORMAdapter().create(make_user_db())
            for i in range(3)
        ]
        usersui = UserUIAdapter().get_all(usersdb)

        AppSettings.objects.create(
            multiuser_mode=True,
            passwordless_login=True,
            show_users_on_login_screen=True,
        )
        auth_store = AppSettingsStore()

        expected = {
            AppSettingsStore.LOGGED_IN_USER: None,
            AppSettingsStore.IS_CONFIGURED: True,
            AppSettingsStore.USER_SELECT_OPTIONS: usersui,
            AppSettingsStore.SHOW_REGISTRATION: True,
            AppSettingsStore.SHOW_PASSWORD_FIELD: False,
            AppSettingsStore.SHOW_USER_SELECT: True,
        }
        returned = auth_store._settings
        self.assertEqual(expected, returned)

    def test_init_settings_false_true_false(self):
        """
        mutliuser_mode = False
        passwordless_login = True
        show_users_on_login_screen = False
        """

        usersdb = [
            UserDBDjangoORMAdapter().create(make_user_db())
            for i in range(3)
        ]
        usersui = UserUIAdapter().get_all(usersdb)

        AppSettings.objects.create(
            multiuser_mode=False,
            passwordless_login=True,
            show_users_on_login_screen=False,
        )
        auth_store = AppSettingsStore()

        expected = {
            AppSettingsStore.LOGGED_IN_USER: usersui[0],
            AppSettingsStore.IS_CONFIGURED: True,
            AppSettingsStore.USER_SELECT_OPTIONS: [],
            AppSettingsStore.SHOW_REGISTRATION: False,
            AppSettingsStore.SHOW_PASSWORD_FIELD: False,
            AppSettingsStore.SHOW_USER_SELECT: False,
        }
        returned = auth_store._settings
        self.assertEqual(expected, returned)

    def test_init_settings_false_true_false_no_users(self):
        """
        mutliuser_mode = False
        passwordless_login = True
        show_users_on_login_screen = False
        """

        AppSettings.objects.create(
            multiuser_mode=False,
            passwordless_login=True,
            show_users_on_login_screen=False,
        )
        auth_store = AppSettingsStore()

        expected = {
            AppSettingsStore.LOGGED_IN_USER: None,
            AppSettingsStore.IS_CONFIGURED: True,
            AppSettingsStore.USER_SELECT_OPTIONS: [],
            AppSettingsStore.SHOW_REGISTRATION: True,
            AppSettingsStore.SHOW_PASSWORD_FIELD: False,
            AppSettingsStore.SHOW_USER_SELECT: False,
        }
        returned = auth_store._settings
        self.assertEqual(expected, returned)

    def test_init_settings_false_true_true(self):
        """
        multiuser_mode = False
        passwordless_login = True
        show_users_on_login_screen = True
        """

        usersdb = [
            UserDBDjangoORMAdapter().create(make_user_db())
            for i in range(3)
        ]
        usersui = UserUIAdapter().get_all(usersdb)

        AppSettings.objects.create(
            multiuser_mode=False,
            passwordless_login=True,
            show_users_on_login_screen=True,
        )
        auth_store = AppSettingsStore()

        expected = {
            AppSettingsStore.LOGGED_IN_USER: usersui[0],
            AppSettingsStore.IS_CONFIGURED: True,
            AppSettingsStore.USER_SELECT_OPTIONS: [],
            AppSettingsStore.SHOW_REGISTRATION: False,
            AppSettingsStore.SHOW_PASSWORD_FIELD: False,
            AppSettingsStore.SHOW_USER_SELECT: False,
        }
        returned = auth_store._settings
        self.assertEqual(expected, returned)

    def test_init_settings_false_false_true(self):
        """
        multiuser_mode = False
        passwordless_login = False
        show_users_on_login_screen = True
        """

        usersdb = [
            UserDBDjangoORMAdapter().create(make_user_db())
            for i in range(3)
        ]
        usersui = UserUIAdapter().get_all(usersdb)

        AppSettings.objects.create(
            multiuser_mode=False,
            passwordless_login=False,
            show_users_on_login_screen=True,
        )
        auth_store = AppSettingsStore()

        expected = {
            AppSettingsStore.LOGGED_IN_USER: None,
            AppSettingsStore.IS_CONFIGURED: True,
            AppSettingsStore.USER_SELECT_OPTIONS: [usersui[0]],
            AppSettingsStore.SHOW_REGISTRATION: False,
            AppSettingsStore.SHOW_PASSWORD_FIELD: True,
            AppSettingsStore.SHOW_USER_SELECT: True,
        }
        returned = auth_store._settings
        self.assertEqual(expected, returned)

    def test_logged_in_user(self):
        auth_store = AppSettingsStore()
        userui = make_user_ui()
        auth_store._settings[AppSettingsStore.LOGGED_IN_USER] = userui

        expected = userui
        returned = auth_store.logged_in_user
        self.assertEqual(expected, returned)

    def test_is_configured(self):
        auth_store = AppSettingsStore()
        auth_store._settings[AppSettingsStore.IS_CONFIGURED] = True

        expected = True
        returned = auth_store.is_configured
        self.assertEqual(expected, returned)

    def test_user_select_options(self):
        auth_store = AppSettingsStore()
        usersui = [make_user_ui() for i in range(3)]
        auth_store._settings[AppSettingsStore.USER_SELECT_OPTIONS] = usersui

        expected = usersui
        returned = auth_store.user_select_options
        self.assertEqual(expected, returned)

    def test_show_registration(self):
        auth_store = AppSettingsStore()
        auth_store._settings[AppSettingsStore.SHOW_REGISTRATION] = True

        expected = True
        returned = auth_store.show_registration
        self.assertEqual(expected, returned)

    def test_show_password_field(self):
        auth_store = AppSettingsStore()
        auth_store._settings[AppSettingsStore.SHOW_PASSWORD_FIELD] = True

        expected = True
        returned = auth_store.show_password_field
        self.assertEqual(expected, returned)

    def test_show_user_select(self):
        auth_store = AppSettingsStore()
        auth_store._settings[AppSettingsStore.SHOW_USER_SELECT] = True

        expected = True
        returned = auth_store.show_user_select
        self.assertEqual(expected, returned)

    def test_login(self):
        auth_store = AppSettingsStore()
        user = make_user_db()
        userdb = UserDBDjangoORMAdapter().create(user)

        expected = UserUIAdapter().get(userdb)
        returned = auth_store.login(user.username, user.password)
        self.assertEqual(expected, returned)

        self.assertEqual(expected, auth_store.get(AppSettingsStore.LOGGED_IN_USER))

    def test_login_user_does_not_exist(self):
        auth_store = AppSettingsStore()
        with self.assertRaises(AuthInvalidError):
            auth_store.login('foo', 'bar')

    def test_login_user_has_no_password(self):
        AppSettings.objects.create(
            multiuser_mode=False,
            passwordless_login=False,
            show_users_on_login_screen=False,
        )
        auth_store = AppSettingsStore()
        user = make_user_db(password=None)
        userdb = UserDBDjangoORMAdapter().create(user)

        with self.assertRaises(AuthInvalidError):
            auth_store.login(user.username, None)

    def test_login_user_has_no_password_and_unconfigured(self):
        auth_store = AppSettingsStore()
        user = make_user_db(password=None)
        userdb = UserDBDjangoORMAdapter().create(user)

        with self.assertRaises(AuthInvalidError):
            auth_store.login(user.username, None)

    def test_login_passwordless_login(self):
        AppSettings.objects.create(
            multiuser_mode=False,
            passwordless_login=True,
            show_users_on_login_screen=False,
        )
        auth_store = AppSettingsStore()

        user = make_user_db(password=None)
        userdb = UserDBDjangoORMAdapter().create(user)

        expected = UserUIAdapter().get(userdb)
        returned = auth_store.login(user.username, None)
        self.assertEqual(expected, returned)

    def test_login_passwordless_login_user_does_not_exist(self):
        AppSettings.objects.create(
            multiuser_mode=False,
            passwordless_login=True,
            show_users_on_login_screen=False,
        )
        auth_store = AppSettingsStore()

        with self.assertRaises(AuthInvalidError):
            auth_store.login('foo', None)

    def test_get(self):
        auth_store = AppSettingsStore()
        for key, value in auth_store._settings.items():
            expected = value
            returned = auth_store.get(key)
            self.assertEqual(expected, returned)

    def test_get_setting_does_not_exist(self):
        auth_store = AppSettingsStore()
        with self.assertRaises(KeyError):
            auth_store.get('foo')

    def test_logout(self):
        auth_store = AppSettingsStore()

        user = make_user_db()
        userdb = UserDBDjangoORMAdapter().create(user)
        userui = auth_store.login(user.username, user.password)

        expected=userui
        returned = auth_store.get(AppSettingsStore.LOGGED_IN_USER)
        self.assertEqual(expected, returned)

        auth_store.logout()
        self.assertIsNone(auth_store.get(AppSettingsStore.LOGGED_IN_USER))

    def test_logout_user_not_logged_in(self):
        auth_store = AppSettingsStore()
        self.assertIsNone(auth_store.get(AppSettingsStore.LOGGED_IN_USER))

        auth_store.logout()
        self.assertIsNone(auth_store.get(AppSettingsStore.LOGGED_IN_USER))
