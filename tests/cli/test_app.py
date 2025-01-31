"""
Copyright (C) J Leadbetter <j@jleadbetter.com>
Affero GPL v3
"""
from asgiref.sync import sync_to_async
from django.test import TestCase

from common.models.app import AppSettingsDB
from common.stores.adapter import AdapterStore
from common.stores.auth import AuthStore
from common.utils.singleton import Singleton

from cli.app import TenThousandWordsApp
from cli.views.login.first_time import FirstTimeModal
from cli.views.login.main import LoginScreen

from ..utils_for_tests.users import make_user_db


class TestTenThousandSentencesApp(TestCase):
    """
    Tests for cli.app.TenThousandWordsApp
    """

    @classmethod
    def setUpClass(cls):
        Singleton.destroy(AdapterStore)
        Singleton.destroy(AuthStore)
        super().setUpClass()

    def tearDown(self):
        Singleton.destroy(AdapterStore)
        Singleton.destroy(AuthStore)

    async def test_on_mount_app_not_configured(self):
        app = TenThousandWordsApp()

        async with app.run_test() as pilot:
            expected = app.get_screen('first_time', FirstTimeModal).name
            returned = app.screen.name
            self.assertEqual(expected, returned)

            # Settings isn't accessible
            await pilot.press('s')
            returned = app.screen.name
            self.assertEqual(expected, returned)

            # Edit mode isn't accessible
            await pilot.press('e')
            returned = app.screen.name
            self.assertEqual(expected, returned)

            # Learn mode isn't accessible
            await pilot.press('l')
            returned = app.screen.name
            self.assertEqual(expected, returned)

            # Trying to log out just redirects to configuration
            await pilot.press('q')
            returned = app.screen.name
            self.assertEqual(expected, returned)

    async def test_on_mount_user_not_logged_in(self):
        adapters = AdapterStore()

        userdb_adapter = adapters.get('UserDBPort')
        userdb = userdb_adapter.create(make_user_db(is_admin=True))

        settings_adapter = adapters.get('AppSettingsPort')
        settings_adapter.create_or_update(AppSettingsDB())

        app = TenThousandWordsApp()
        async with app.run_test() as pilot:
            expected = app.get_screen('login', LoginScreen).name
            returned = app.screen.name
            self.assertEqual(expected, returned)

            # Settings isn't accessible
            await pilot.press('s')
            returned = app.screen.name
            self.assertEqual(expected, returned)

            # Edit mode isn't accessible
            await pilot.press('e')
            returned = app.screen.name
            self.assertEqual(expected, returned)

            # Learn mode isn't accessible
            await pilot.press('l')
            returned = app.screen.name
            self.assertEqual(expected, returned)

            # Trying to log out just redirects login screen
            await pilot.press('q')
            returned = app.screen.name
            self.assertEqual(expected, returned)

    async def test_on_mount_user_logged_in(self):
        pass
