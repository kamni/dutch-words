"""
Copyright (C) J Leadbetter <j@jleadbetter.com>
Affero GPL v3
"""

from pydantic import BaseModel


class AudioFile(BaseModel):
    """
    Representation of an audio file in the database.

    Used with the TTS Port
    """

    id: Optional[str] = None  # UUID; string allows for serialization to JSON
    languageCode: str
    text: str
    file_path: str
