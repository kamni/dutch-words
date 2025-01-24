"""
Copyright (C) J Leadbetter <j@jleadbetter.com>
Affero GPL v3
"""

from typing import List, Optional

from pydantic import BaseModel

#from common.models.session import UserSession
from common.models.users import User
from common.models.words import Word


class Database(BaseModel):
    """
    Representation of the database.
    Only for use with the JSON adapters (for development only).
    DO NOT USE IN PRODUCTION.
    """

    users: Optional[List[User]] = []
    words: Optional[List[Word]] = []
