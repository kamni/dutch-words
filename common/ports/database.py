"""
Copyright (C) J Leadbetter <j@jleadbetter.com>
Affero GPL v3

Port for managing the database.
"""

from abc import ABC, abstractmethod


class DatabaseError(Exception):
    """
    Throw this error when there are issues connecting to the database
    """
    pass


class DatabasePort(ABC):
    """
    Commands to manage the app database
    """

    def initialize_database(self):
        """
        Set up the expected tables in the database.
        Ignores if tables already exist.

        :raises: DatabaseError if something goes wrong.
        """
        pass

    @abstractmethod
    def teardown_database(self):
        """
        Drop all tables in the database.
        Ignores if database isn't there.

        :raises: DatabaseError if something goes wrong.
        """
        pass
