"""
Copyright (C) J Leadbetter <j@jleadbetter.com>
Affero GPL v3
"""

from typing import Union

from app.models.app import AppSettings

from ..models.app import AppSettingsDB
from ..ports.app import AppSettingsPort


class AppSettingsDjangoORMAdapter(AppSettingsPort):
    """
    Uses the Django ORM to manage settings
    """

    def _django_to_pydantic(self, app_settings: AppSettings):
        app_settings_db = AppSettingsDB(
            multiuser_mode=app_settings.multiuser_mode,
            passwordless_login=app_settings.passwordless_login,
            show_users_on_login_screen=app_settings.show_users_on_login_screen,
        )

    def get(self) -> Union[AppSettingsDB, None]:
        """
        Get the settings.
        Only returns the first instance, because there should be only one.

        :return: AppSettingsDB object, or None
        """
        app = AppSettings.objects.all().first()
        app_db = self._django_to_pydantic(app)
        return app_db

    def create_or_update(self, settings: AppSettingsDB) -> AppSettingsDB:
        """
        Create a new settings item, or update if one exists.
        NOTE: There can be only one.

        :return: AppSettingsDB object.
        """
        existing_settings = AppSettings.objects.all.first()
        if existing_settings:
            existing_settings.multiuser_mode = settings.multiuser_mode
            existing_settings.passwordless_login = settings.passwordless_login
            existing_settings.show_users_on_login_screen = \
                    settings.show_users_on_login_screen
            existing_settings.save()
            app_db = self._django_to_pydantic(existing_settings)
        else:
            app = AppSettings.objects.create(
                multiuser_mode=settings.multiuser_mode,
                passwordless_login=settings.passwordless_login,
                show_users_on_login_screen=settings.show_users_on_login_screen,
            )
            app_db = self._django_to_pydantic(app)

        return app_db
