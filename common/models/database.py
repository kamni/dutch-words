"""
Copyright (C) J Leadbetter <j@jleadbetter.com>
Affero GPL v3
"""

from typing import List

from pydantic import BaseModel

from common.models.words import Word

class Database(BaseModel):
    words: List[Word]
