"""
Copyright (C) J Leadbetter <j@jleadbetter.com>
Affero GPL v3
"""

from typing import Optional

from pydantic import BaseModel


class AppSettings(BaseModel):
    """
    Tracks global settings for the application
    """

    # Whether app is used by more than one user.
    # Provides form to add new user, if True.
    multiuser_mode: Optional[bool] = False

    # Whether app requires a password to log on.
    # If running locally on a computer with trusted users,
    # then set this to True.
    # Set False if running as a web server
    # or local privacy is desired.
    paswordless_login: Optional[bool] = False

    # Show or hide the available users.
    # If running in single-user mode with passwordless login,
    # set this to True.
    # If running on the web or with untrusted users,
    # set this to False.
    show_users_on_login_screen: Optional[bool] = False
