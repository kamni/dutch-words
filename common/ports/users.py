"""
Copyright (C) J Leadbetter <j@jleadbetter.com>
Affero GPL v3

Port for working with Users
"""

from abc import ABC, abstractmethod
from typing import List

from common.models.users import User


class UserPort(ABC):
    """
    Manages users in the database
    """

    @abstractmethod
    def create(self, user: User) -> User:
        """
        Create a new user in the database.

        :user: New User object to add to the database.
            User is counted as a duplicate when it has the same
            languageCode and baseUser.

        :return: Created User object.
        :raises: ObjectExistsError if the object already exists.
        """
        pass

    @abstractmethod
    def create_in_batch(self, users: List[User]) -> List[User]:
        """
        Batch create multiple users.
        Ignores users that already exist.

        :user: New User object to add to the database.
            User is counted as a duplicate when it has the same
            languageCode and baseUser.

        :return: List of created users.
            Returns None for any users that were not created,
            so the lists can be compared, if needed.
        """
        pass
