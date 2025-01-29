"""
Copyright (C) J Leadbetter <j@jleadbetter.com>
Affero GPL v3
"""

from django.contrib.auth.models import User
from django.test import TestCase

from common.adapters.auth import AuthnDjangoORMAdapter
from common.models.users import UserUI, UserDB
from common.ports.auth import AuthnInvalidError
from common.stores.adapter import AdapterStore


class TestAuthnDjangoORMAdapter(TestCase):
    """
    Tests for common.adapters.auth.AuthnDjangoORMAdapter
    """

    @classmethod
    def setUpClass(cls):
        adapters = AdapterStore(subsection='dev.django')
        adapters.initialize()

        cls.auth_adapter = adapters.get('AuthnPort')
        cls.user_db_adapter = adapters.get('UserDBPort')
        cls.user_ui_adapter = adapters.get('UserUIPort')
        super().setUpClass()

    def test_login(self):
        user = UserDB(
            username='test_login',
            password='1234567',
            display_name='Test User',
        )
        userdb = self.user_db_adapter.create(user)

        expected = self.user_ui_adapter.get(userdb)
        returned = self.auth_adapter.login(user.username, user.password)
        self.assertEqual(expected, returned)

    def test_login_user_does_not_exist(self):
        with self.assertRaises(AuthnInvalidError):
            self.auth_adapter.login('foo', 'bar')

    def test_login_user_does_not_have_settings(self):
        # This might happen if an admin user was created
        # for the django admin
        username = 'test_login_user_no_settings'
        password = '1234567'
        user = User.objects.create(username=username)
        user.set_password(password)
        user.save()

        with self.assertRaises(AuthnInvalidError):
            self.auth_adapter.login(username, password)

    def test_logout(self):
        pass

    def test_logout_user_does_not_exist(self):
        pass
