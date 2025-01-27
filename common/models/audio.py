"""
Copyright (C) J Leadbetter <j@jleadbetter.com>
Affero GPL v3
"""

from typing import Optional

from pydantic import BaseModel

from ..utils.languages import LanguageCode


class AudioFileUI(BaseModel):
    """
    Representation of an audio file in the UI.
    """

    languageCode: LanguageCode
    text: str
    file_path: str

    @property
    def unique_together(self):
        return ['file_path']
