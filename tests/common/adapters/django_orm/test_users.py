"""
Copyright (C) J Leadbetter <j@jleadbetter.com>
Affero GPL v3
"""

import uuid

from django.test import TestCase

from common.adapters.django_orm.users import (
    UserDBDjangoORMAdapter,
    UserUIDjangoORMAdapter,
)
from common.models.errors import ObjectExistsError, ObjectNotFoundError
from common.models.users import UserDB, UserUI
from common.stores.adapter import AdapterStore

from users.models.settings import UserSettings


class TestUserDBDjangoORMAdapter(TestCase):
    """
    Tests for backend.words.adapters.users.UserDBDjangoORMAdapter
    """

    @classmethod
    def setUpClass(cls):
        adapters = AdapterStore(subsection='dev.django')
        cls.adapter = adapters.get('UserDBPort')
        super().setUpClass()

    def test_create(self):
        user = UserDB(
            username='test_create_user',
            password='1234567',
            display_name='Test User',
        )

        # Check the returned object
        new_user = self.adapter.create(user)
        self.assertIsNotNone(new_user.id)
        self.assertFalse(new_user.password)  # We don't return passwords
        self.assertEqual(user.username, new_user.username)
        self.assertEqual(user.display_name, new_user.display_name)
        self.assertNotEqual(user.password, new_user.password)

        # Verify the database object
        new_db_user = UserSettings.objects.get(id=new_user.id)
        self.assertTrue(new_db_user.password)
        self.assertEqual(new_user.username, new_db_user.username)
        self.assertEqual(new_user.display_name, new_db_user.display_name)

    def test_create_without_password(self):
        user = UserDB(
            username='test_create_user_no_password',
            display_name='Test User',
        )

        # Check the returned object
        new_user = self.adapter.create(user)
        self.assertIsNotNone(new_user.id)
        self.assertFalse(new_user.password)  # empty string
        self.assertEqual(user.username, new_user.username)
        self.assertEqual(user.display_name, new_user.display_name)

        # Verify the database object
        new_db_user = UserSettings.objects.get(id=new_user.id)
        self.assertFalse(new_db_user.password)  # empty string
        self.assertEqual(new_user.username, new_db_user.username)
        self.assertEqual(new_user.display_name, new_db_user.display_name)

    def test_create_admin(self):
        user = UserDB(
            username='test_create_admin',
            password='1234567',
            display_name='Test User',
            is_admin=True,
        )
        userdb = self.adapter.create(user)

        new_user = UserSettings.objects.get(id=userdb.id)
        self.assertTrue(new_user.is_admin)

    def test_create_duplicate_user(self):
        user = UserDB(
            username='test_create_user_duplicate_django_user',
            password='1234567',
            display_name='Test User',
        )
        self.adapter.create(user)

        with self.assertRaises(ObjectExistsError):
            self.adapter.create(user)

    def test_get(self):
        user = UserDB(
            username='test_get',
            password='1234567',
            display_name='Test User',
        )
        new_user = self.adapter.create(user)

        new_user_db = self.adapter.get(new_user.id)
        self.assertEqual(new_user, new_user_db)

    def test_get_user_settings_does_not_exist(self):
        user_id = uuid.uuid4()

        with self.assertRaises(ObjectNotFoundError):
            self.adapter.get(user_id)

    def test_get_user_is_active_false(self):
        user = UserDB(
            username='test_get_inactive',
            password='1234567',
            display_name='Test User',
        )
        userdb = self.adapter.create(user)
        settings = UserSettings.objects.get(id=userdb.id)
        settings.user.is_active = False
        settings.user.save()

        with self.assertRaises(ObjectNotFoundError):
            self.adapter.get(userdb.id)

    def test_get_first(self):
        user = UserDB(
            username='test_get_first',
            password='1234567',
            display_name='Test User',
        )
        self.adapter.create(user)

        expected = user
        returned = self.adapter.get_first()
        self.assertEqual(expected, returned)

    def test_get_first_database_empty(self):
        self.assertIsNone(self.adapter.get_first())

    def test_get_first_more_than_one(self):
        user1 = UserDB(
            username='test_get_first_more_than_one1',
            password='1234567',
            display_name='Test User',
        )
        self.adapter.create(user1)

        user2 = UserDB(
            username='test_get_first_more_than_one2',
            password='1234567',
            display_name='Test User',
        )
        self.adapter.create(user2)

        expected = user1
        returned = self.adapter.get_first()
        self.assertEqual(expected, returned)

    def test_get_first_is_active_false(self):
        user = UserDB(
            username='test_get_first_inactive',
            password='1234567',
            display_name='Test User',
        )
        userdb = self.adapter.create(user)

        expected = userdb
        returned = self.adapter.get_first()
        self.assertEqual(expected, returned)

        settings = UserSettings.objects.get(id=userdb.id)
        settings.user.is_active = False
        settings.user.save()

        self.assertIsNone(self.adapter.get_first())

    def test_get_by_username(self):
        username = 'test_get_by_username'
        user = UserDB(
            username=username,
            password='1234567',
            display_name='Test User',
        )

        new_user = self.adapter.create(user)
        new_user_db = self.adapter.get_by_username(username)
        self.assertEqual(new_user, new_user_db)

    def test_get_by_username_settings_does_not_exist(self):
        username = 'nonexistent_username'

        with self.assertRaises(ObjectNotFoundError):
            self.adapter.get_by_username(username)

    def test_get_by_username_user_inactive(self):
        user = UserDB(
            username='test_get_username_inactive',
            password='1234567',
            display_name='Test User',
        )
        userdb = self.adapter.create(user)

        settings = UserSettings.objects.get(id=userdb.id)
        settings.user.is_active = False
        settings.user.save()

        with self.assertRaises(ObjectNotFoundError):
            self.assertIsNone(self.adapter.get_by_username(userdb.username))

    def test_get_all(self):
        user1 = UserDB(
            username='test_get_all1',
            password='1234567',
            display_name='Test User',
        )
        self.adapter.create(user1)

        user2 = UserDB(
            username='test_get_all2',
            password='1234567',
            display_name='Test User',
        )
        self.adapter.create(user2)

        # ignore this user
        user3 = UserDB(
            username='test_get_all3',
            password='1234567',
            display_name='Test User',
        )
        userdb3 = self.adapter.create(user3)
        settings = UserSettings.objects.get(id=userdb3.id)
        settings.user.is_active = False
        settings.user.save()

        expected = [user1, user2]
        returned = self.adapter.get_all()
        self.assertEqual(expected, returned)

    def test_get_all_table_empty(self):
        expected = []
        returned = self.adapter.get_all()
        self.assertEqual(expected, returned)

    def test_update(self):
        userdb = UserDB(
            username='test_update',
            password='1234567',
            display_name='Test User',
        )
        new_userdb = self.adapter.create(userdb)
        old_password = UserSettings.objects.get(id=new_userdb.id).password

        new_userdb.is_admin = True
        new_userdb.display_name = 'New Test User'
        new_userdb.password = 'foo'
        new_userdb.username = 'Should not change!'

        final_userdb = self.adapter.update(new_userdb)
        new_password = UserSettings.objects.get(id=new_userdb.id).password
        self.assertNotEqual(old_password, new_password)
        self.assertEqual(new_userdb.display_name, final_userdb.display_name)
        self.assertEqual(userdb.username, final_userdb.username)
        self.assertTrue(final_userdb.is_admin)

    def test_update_does_not_exist(self):
        userdb = UserDB(
            id=uuid.uuid4(),
            username='test_update_not_exists',
            password='1234567',
            display_name='Test User',
        )
        with self.assertRaises(ObjectNotFoundError):
            self.adapter.update(userdb)


class TestUserUIDjangoORMAdapter(TestCase):
    """
    Tests for backend.words.adapters.users.UserUIDjangoORMAdapter
    """

    @classmethod
    def setUpClass(cls):
        adapters = AdapterStore(subsection='dev.django')
        cls.adapter = adapters.get('UserUIPort')
        super().setUpClass()

    def test_get(self):
        user_db = UserDB(
            username='test_get',
            password='1234567',
            display_name='Test User',
        )
        db_adapter = UserDBDjangoORMAdapter()
        new_user_db = db_adapter.create(user_db)

        expected = UserUI(
            id=new_user_db.id,
            username=new_user_db.username,
            displayName=new_user_db.display_name,
        )
        returned = self.adapter.get(new_user_db)
        self.assertEqual(expected, returned)

    def test_get_with_no_display_name(self):
        user_db = UserDB(
            username='test_get_no_display_name',
            password='1234567',
        )
        db_adapter = UserDBDjangoORMAdapter()
        new_user_db = db_adapter.create(user_db)

        expected = UserUI(
            id=new_user_db.id,
            username=new_user_db.username,
            displayName=new_user_db.username,
        )
        returned = self.adapter.get(new_user_db)
        self.assertEqual(expected, returned)

    def test_get_all(self):
        user_db1 = UserDB(
            id=uuid.uuid4(),
            username='test_get_all1',
            password='1234567',
            display_name='Test User'
        )
        user_db2 = UserDB(
            id=uuid.uuid4(),
            username='test_get_all2',
            password='1234567',
        )

        expected = [
            UserUI(
                id=user_db1.id,
                username=user_db1.username,
                displayName=user_db1.display_name,
            ),
            UserUI(
                id=user_db2.id,
                username=user_db2.username,
                displayName=user_db2.username,
            ),
        ]
        returned = self.adapter.get_all([user_db1, user_db2])
        self.assertEqual(expected, returned)

    def test_get_all_empty_list(self):
        expected = []
        returned = self.adapter.get_all([])
        self.assertEqual(expected, returned)
