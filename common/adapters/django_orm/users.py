"""
Copyright (C) J Leadbetter <j@jleadbetter.com>
Affero GPL v3
"""

from typing import List, Union

from django.contrib.auth.models import User
from django.db.utils import IntegrityError

from users.models.settings import UserSettings

from ...models.errors import ObjectExistsError, ObjectNotFoundError
from ...models.users import UserDB, UserUI
from ...ports.users import UserDBPort, UserUIPort


class UserDBDjangoORMAdapter(UserDBPort):
    """
    Handles CRUD for users in the database
    """

    def __init__(self, **kwargs):
        # Ignore any kwargs configuration.
        # This uses the django settings.
        super().__init__()

    def _django_to_pydantic(self, user: UserSettings) -> UserDB:
        # We don't return the password here,
        # because the hash is relatively useless to us.
        pydantic_user = UserDB(
            id=user.id,
            username=user.username,
            display_name=user.display_name,
            is_admin=user.is_admin,
        )
        return pydantic_user

    def create(self, user: UserDB) -> UserDB:
        """
        Create a new user in the database.

        :user: New user to add to the database.

        :return: Created user object.
        :raises: ObjectExistsError if the object already exists.
        """

        try:
            new_user = User.objects.create(
                username=user.username,
                is_superuser=user.is_admin,
            )
        except IntegrityError as exc:
            raise ObjectExistsError(exc)

        if user.password:
            new_user.set_password(user.password)
            new_user.save()

        # The user is unique on a UserSettings model.
        # We don't have to worry about a duplicate user,
        # because it would have failed in the previous try-except block.
        new_settings = UserSettings.objects.create(
            user=new_user,
            display_name=user.display_name,
        )

        new_user_db = self._django_to_pydantic(new_settings)
        return new_user_db

    def get(self, id: str) -> UserDB:
        """
        Get a user from the database using an ID.

        :id: User's UUID.

        :return: Found user object.
        :raises: ObjectNotFoundError if the user does not exist.
        """

        try:
            settings = UserSettings.objects.get(
                id=id,
                user__is_active=True,
            )
        except UserSettings.DoesNotExist as exc:
            raise ObjectNotFoundError(exc)

        user = self._django_to_pydantic(settings)
        return user

    def get_first(self) -> Union[UserDB, None]:
        """
        Get the first user in the database.
        Useful as a default when not using a multi-user system

        :return: First user in the database; None if there are no users.
        """

        user = UserSettings.objects.filter(
            user__is_active=True,
        ).first()
        userdb = self._django_to_pydantic(user) if user else None
        return userdb

    def get_by_username(self, username: str) -> UserDB:
        """
        Get a user from the database using a username.

        :username: User's username

        :return: Found user object.
        :raises: ObjectNotFoundError
        """

        try:
            settings = UserSettings.objects.get(
                user__username=username,
                user__is_active=True,
            )
        except UserSettings.DoesNotExist as exc:
            raise ObjectNotFoundError(exc)

        user = self._django_to_pydantic(settings)
        return user

    def get_all(self) -> List[UserDB]:
        """
        Get all users from the database.

        :return: List of user objects (may be empty)
        """
        users = UserSettings.objects.filter(user__is_active=True)
        usersdb = [self._django_to_pydantic(user) for user in users]
        return usersdb

    def update(self, user: UserDB) -> UserDB:
        """
        Update an existing user.

        Not all fields are editable.
        Here's what you can edit:

        * display_name
        * password
        * is_admin

        :user: UserDB instance to update.
            Must have id.

        :return: Updated UserDB object
        :raises: ObjectNotFoundError
        """

        try:
            userdb = UserSettings.objects.get(id=user.id)
        except Exception as exc:
            raise ObjectNotFoundError(exc)

        userdb.display_name = user.display_name
        userdb.user.is_superuser = user.is_admin
        if user.password:
            userdb.user.set_password(user.password)

        userdb.user.save()
        userdb.save()

        updated_user = UserSettings.objects.get(id=user.id)
        updated_user_db = self._django_to_pydantic(updated_user)
        return updated_user_db


class UserUIDjangoORMAdapter(UserUIPort):
    """
    Works with user objects for the UI
    """

    def __init__(self, **kwargs):
        # Ignore any kwargs configuration.
        # This uses the django settings.
        super().__init__()

    def _db_to_ui(self, user: UserDB) -> UserUI:
        user_ui = UserUI(
            id=user.id,
            username=user.username,
            displayName=user.display_name or user.username,
            isAdmin=user.is_admin,
        )
        return user_ui

    def get(self, user: UserDB) -> UserUI:
        """
        Convert a database user into a UI user.

        :user: Database representation of a user.

        :return: UI representation of a user.
        """
        user_ui = self._db_to_ui(user)
        return user_ui

    def get_all(self, users: List[UserDB]) -> List[UserUI]:
        """
        Convert all database users to users for the UI.

        :users: List of database representations of users.

        :return: List of UI representations of the users.
        """

        usersui = [self._db_to_ui(user) for user in users]
        return usersui
