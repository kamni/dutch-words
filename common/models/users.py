"""
Copyright (C) J Leadbetter <j@jleadbetter.com>
Affero GPL v3
"""

import time
import uuid
from typing import Any, Optional

from pydantic import BaseModel


class User(BaseModel):
    """
    Representation of a user in the database.
    """

    id: Optional[str] = None
    username: str
    password: Optional[str] = None
    display_name: str

    def __hash__(self):
        return hash(self.username)

    def __eq__(self, other: Any) -> bool: 
        """
        Two users are equal if the usernames are equal
        """
        if isinstance(other, BaseModel): 
            self_type = self.__pydantic_generic_metadata__['origin'] or self.__class__
            other_type = other.__pydantic_generic_metadata__['origin'] or other.__class__

            return (
                self_type == other_type and (
                    self.__dict__ == other.__dict__ or
                    self.username == other.username
                )
            )
        return False


class UserDisplay(BaseModel):
    """
    Representation of a logged-in user in the UI.
    NOTE: use camel-cased attributes for easier handling with javascript
    """

    user_id: Optional[str] = None
    username: str
    displayName: Optional[str] = None

    @classmethod
    def from_user(cls, user: User) -> 'UserDisplay':
        """
        Convert a database user into a UI-friendly user object.

        :user: User object from the database
        :return: UserDisplay for the UI.
        """

        user_display = UserDisplay(
            user_id=user.id,
            username=user.username,
            displayName=user.display_name or user.username,
        )
        return user_display
