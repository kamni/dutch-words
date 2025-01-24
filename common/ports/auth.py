"""
Copyright (C) J Leadbetter <j@jleadbetter.com>
Affero GPL v3

Interfaces for authentication and authentication
"""

from abc import ABC, abstractmethod

from common.models.users import UserDisplay


class AuthError(Exception):
    pass


class AuthValidationError(Exception):
    pass


class AuthnPort(ABC):
    """
    Authenticate a user for the system
    """

    # TODO: handling of token refresh, sessions, etc.
    # For right now, just working with the json database.

    @abstractmethod
    def login(self, username: str, password: str) -> UserDisplay:
        """
        Log the user into the system.

        :username: username of the person logging in.
        :password: password of the person loggint in.

        :return: UserDisplay for the UI
        :raises: AuthError for problems communicating with the authn backend;
            AuthValidationError when authentication is invalid.
        """
        pass

    @abstractmethod
    def logout(self, user: UserDisplay) -> bool:
        """
        Logs a user out of the system.

        :user: Currently logged-in user.

        :return: True if successful, False if already logged out
        :raises: AuthError for problems communicating with the authn backend.
        """
        pass
