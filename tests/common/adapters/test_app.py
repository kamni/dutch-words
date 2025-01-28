"""
Copyright (C) J Leadbetter <j@jleadbetter.com>
Affero GPL v3
"""

from django.test import TestCase

from app.models.app import AppSettings
from common.adapters.app import AppSettingsDjangoORMAdapter
from common.models.app import AppSettingsDB


class TestAppSettingsDjangoORMAdapter(TestCase):
    """
    Tests for common.adapters.app.AppSettingsDjangoORMAdapter
    """

    def tearDown(self):
        AppSettings.objects.all().delete()

    def test_get(self):
        app_db = AppSettingsDB(
            multiuser_mode=True,
            passwordless_login=False,
            show_users_on_login_screen=True,
        )
        adapter = AppSettingsDjangoORMAdapter()
        AppSettings.objects.create(**app_db.model_dump())

        expected = app_db
        returned = adapter.get()
        self.assertEqual(expected, returned)

    def test_get_does_not_exist(self):
        adapter = AppSettingsDjangoORMAdapter()
        self.assertIsNone(adapter.get())

    def test_get_when_multiple_exist(self):
        app_db1 = AppSettingsDB(
            multiuser_mode=False,
            passwordless_login=True,
            show_users_on_login_screen=False,
        )
        AppSettings.objects.create(**app_db1.model_dump())

        app_db2 = AppSettingsDB(
            multiuser_mode=True,
            passwordless_login=True,
            show_users_on_login_screen=True,
        )
        AppSettings.objects.create(**app_db2.model_dump())

        adapter = AppSettingsDjangoORMAdapter()
        expected = app_db1
        returned = adapter.get()
        self.assertEqual(expected, returned)
        self.assertNotEqual(app_db2, returned)

    def test_create_or_update_when_created(self):
        app_db = AppSettingsDB(
            multiuser_mode=True,
            passwordless_login=False,
            show_users_on_login_screen=False,
        )
        adapter = AppSettingsDjangoORMAdapter()

        expected = app_db
        returned1 = adapter.create_or_update(app_db)
        self.assertEqual(expected, returned1)

        returned2 = adapter.get()
        self.assertEqual(expected, returned2)

    def test_create_or_update_when_updated(self):
        app_db1 = AppSettingsDB(
            multiuser_mode=False,
            passwordless_login=True,
            show_users_on_login_screen=False,
        )
        AppSettings.objects.create(**app_db1.model_dump())
        adapter = AppSettingsDjangoORMAdapter()

        app_db2 = AppSettingsDB(
            multiuser_mode=True,
            passwordless_login=True,
            show_users_on_login_screen=False,
        )

        expected = app_db2
        returned = adapter.create_or_update(app_db2)
        self.assertEqual(expected, returned)
        self.assertEqual(1, AppSettings.objects.count())
