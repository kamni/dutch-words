"""
Copyright (C) J Leadbetter <j@jleadbetter.com>
Affero GPL v3
"""

from django.contrib.auth.models import User
from django.test import TestCase

from common.adapters.auth import AuthnDjangoORMAdapter
from common.models.users import UserUI, UserDB
from common.stores.adapter import AdapterStore


class TestAuthnDjangoORMAdapter(TestCase):
    """
    Tests for common.adapters.auth.AuthnDjangoORMAdapter
    """

    @classmethod
    def setUpClass(cls):
        adapters = AdapterStore(subsection='dev.django')
        adapters.initialize()

        self.auth_adapter = adapters.get('AuthnPort')
        self.user_db_adapter = adapters.get('UserDBPort')
        self.user_ui_adapter = adapters.get('UserUIPort')
        super().setUpClass()

    def test_login(self):
        user = UserDB(
            username='test_login',
            password='1234567',
            display_name='Test User',
        )
        userdb = self._user_db_adapter.create(user)

        expected = self.user_ui_adapter.get(userdb)
        returned = self.auth_adapter.login(user.username, user.password)
        self.assertEqual(expected, returned)

    def test_login_user_does_not_exist(self):
        pass

    def test_login_user_does_not_have_settings(self):
        # Admin
        pass

    def test_logout(self):
        pass

    def test_logout_user_does_not_exist(self):
        pass
