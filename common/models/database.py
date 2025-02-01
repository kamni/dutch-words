"""
Copyright (C) J Leadbetter <j@jleadbetter.com>
Affero GPL v3
"""

from typing import List, Optional

from pydantic import BaseModel

from ..models.documents import DocumentDB
from ..models.users import UserDB
from ..models.words import WordDB


class Database(BaseModel):
    """
    Representation of the database.
    Only for use with the JSON adapters (for development only).
    DO NOT USE IN PRODUCTION.
    """

    users: Optional[List[UserDB]] = []
    documents: Optional[List[DocumentDB]] = []
    words: Optional[List[WordDB]] = []
