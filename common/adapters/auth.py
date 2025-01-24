"""
Copyright (C) J Leadbetter <j@jleadbetter.com>
Affero GPL v3

Implementations of AuthenticationPort.
"""

import hashlib

from common.adapters.users import UserJSONFileAdapter
from common.models.errors import ObjectNotFoundError
from common.stores.adapter import AdapterStore
from common.models.users import User, UserDisplay
from common.ports.auth import AuthnPort, AuthError, AuthValidationError


class AuthnJSONFileAdapter(AuthnPort):
    """
    Authentication handler for JSON file database.

    WARNING: This is only intended for local development.
    DO NOT USE IN PRODUCTION ENVIRONMENTS.
    """

    _user_port = None

    def __init__(self, **kwargs):
        # We don't need any of the usual kwargs.
        pass

    @property
    def user_port(self):
        if not self._user_port:
            adapters = AdapterStore()
            adapters.initialize()
            self._user_port = adapters.get('UserPort')
        return self._user_port

    def _password_valid(self, user: User, password: str) -> bool:
        # REMINDER: don't use this adapter in production!!
        divider = user.password.index('$')
        psalt = user.password[:divider]
        phash = user.password[divider+1:]

        pswd_str = f'{psalt}{password}'.encode('utf-8')
        vhash = hashlib.sha256(pswd_str).hexdigest()
        is_valid = vhash == phash
        return is_valid

    def login(self, username: str, password: str) -> UserDisplay:
        """
        Log the user into the system.

        :username: username of the person logging in.
        :password: password of the person loggint in.

        :return: UserDisplay for the UI
        :raises: AuthError for problems communicating with the authn backend;
            AuthValidationError when authentication is invalid.
        """
        try:
            user = self.user_port.read(username=username)
        except ObjectNotFoundError:
            # Error information for logging purposes only.
            # Don't display to user
            raise AuthValidationError('Invalid login: user not found')
        except Exception as ex:
            raise AuthError(f'ERROR: {ex}')

        if self._password_valid(user, password):
            user_display = UserDisplay.from_user(user)
            return user_display
        else:
            # Error information for logging purposes only.
            # Don't display to user
            raise AuthValidationError('Invalid login: bad password')

    def logout(self, user_display: UserDisplay) -> bool:
        """
        Logs a user out of the system.

        :user: Currently logged-in user.

        :return: True if successful, False if already logged out
        :raises: AuthError for problems communicating with the authn backend.
        """

        try:
            user = self.user_port.read(username=user_display.username)
            session = self.user_port.read_session(user)
        except ObjectNotFoundError:
            raise AuthError('ERROR: unknown')
        except Exception as ex:
            raise AuthError(f'ERROR: {ex}')


