"""
Copyright (C) J Leadbetter <j@jleadbetter.com>
Affero GPL v3
"""

from django.contrib.auth import authenticate, login

from ..models.errors import ObjectNotFoundError
from ..ports.auth import AuthnInvalidError, AuthnPort
from ..stores.adapter import AdapterStore


class AuthnDjangoORMAdapter(ABC):
    """
    Handles authentication of a user using the Django ORM.

    NOTE: This adapter presumes that it is running locally
          as a desktop application.
          This authenticates directly with the Django database,
          and does not rely on http requests.
          For this reason the logged-in status of the user
          is managed by the in-memory common.stores.auth.AuthStore
          and not via Django requests.

          Please create an AuthDjangoAPIAdapter
          if you wish to authenticate via http requests
          and let Django manage the session.
    """
    def __init__(self, **kwargs):
        # Ignore any kwargs configuration.
        # This uses the django settings.
        super().__init__()

        adapters = AdapterStore()
        self._user_db_adapter = adapters.get('UserDBPort')
        self._user_ui_adapter = adapters.get('UserUIPort')

    @abstractmethod
    def login(self, username: str, password: str) -> UserUI:
        """
        Log a user in.

        :username: Username of the user.
        :password: Password of the user.

        :return: UserUI:
        :raises: AuthnInvalidError if user is not sucessfully authenticated.
        """
        user = authenticate(
            request=None,
            username=username,
            password=password,
        )
        if not user:
            # This message is only for internal logging.
            # Do not show the message to users,
            # as it reveals the internals of the system
            # and may encourage hacking.
            raise AuthnInvalidError('Failed to authenticate with Django')

        try:
            userdb = self._user_db_adapter.get_by_username(username)
        except ObjectNotFoundError:
            # This message is only for internal logging.
            # Do not show to users.
            raise AuthnInvalidError('Django user found, but UserSettings missing')

        userui = self._user_ui_adapter.get(userdb)

    @abstractmethod
    def logout(self, user: UserUI):
        """
        Log a user out.
        Should not error if user is no longer logged in
        or was never logged in.

        :user: UserUI object that was logged in
        """
        # Nothing to do.
        # The AuthStore is handling the "session"
        return None
