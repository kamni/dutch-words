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

    @classmethod
    def make_user(self, username: str, password: str, display_name: Optional[str] = None):
        """
        Preferred method of creating a User from inputted data.
        Sets the id and password.

        :username: User's username in the system. Should be unique.
        :password: Plaintext password. Will be salted and hashed before
            storing to the database.
        :display_name: Optional display name for the User.
            Does not have to be unique.
        """

        user = User(username=username, display_name=display_name)
        user.set_id()
        user.set_password(password)
        return user

    def set_id(self):
        """
        Set the id for the Word and all ids for the type.
        """
        if not self.id:
            self.id = str(uuid.uuid4())

    def set_password(self, password: str):
        salt = time.monotonic()
        phash = hash(f'{salt}{password}')
        self.password = f'{salt}${phash}'


class UserDisplay(BaseModel):
    """
    Representation of a logged-in user in the UI.
    NOTE: use camel-cased attributes for easier handling with javascript
    """

    user_id: Optional[str]
    username: str
    displayName: Optional[str] = None

    def from_user(self, user: User) -> 'UserDisplay':
        """
        Convert a database user into a UI-friendly user object.

        :user: User object from the database
        :return: UserDisplay for the UI.
        """

        user_display = UserDisplay(
            username=user.username,
            displayName=user.display_name or user.username,
        )
        return user_display
