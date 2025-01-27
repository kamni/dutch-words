"""
Copyright (C) J Leadbetter <j@jleadbetter.com>
Affero GPL v3

Port for working with UserDBs
"""

from abc import ABC, abstractmethod
from typing import List

from common.models.users import UserDB


class UserPort(ABC):
    """
    Manages users in the database
    """

    @abstractmethod
    def create(self, user: UserDB) -> UserDB:
        """
        Create a new user in the database.

        :user: New UserDB object to add to the database.
            UserDB is counted as a duplicate when it has the same
            languageCode and baseUserDB.

        :return: Created UserDB object.
        :raises: ObjectExistsError if the object already exists.
        """
        pass

    @abstractmethod
    def create_in_batch(self, users: List[UserDB]) -> List[UserDB]:
        """
        Batch create multiple users.
        Ignores users that already exist.

        :user: New UserDB object to add to the database.
            UserDB is counted as a duplicate when it has the same
            languageCode and baseUserDB.

        :return: List of created users.
            Returns None for any users that were not created,
            so the lists can be compared, if needed.
        """
        pass

    @abstractmethod
    def read(self, username: str) -> UserDB:
        """
        Read a single UserDB from the database.

        :username: The username to search for.
            UserDBname is expected to be unique.

        :return: The user that was found.
        :raises: ObjectNotFoundError if user doesn't exist
        """
        pass
