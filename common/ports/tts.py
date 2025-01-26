"""
Copyright (C) J Leadbetter <j@jleadbetter.com>
Affero GPL v3
"""

from abc import ABC, abstractmethod

from ..models.audio import AudioFile


class TTSPort(ABC):
    """
    Handles text-to-speech
    """

    @abstractmethod
    class create(self, audio_file: AudioFile):
        """
        Creates an audio file using a text-to-speech engine

        :audio_file: new AudioFile object to add to the database.
            AudioFile is counted as a duplicate when it has the same
            languageCode and text.

        :return: Created AudioFile object.
        :raises ObjectExistsError if the object already exists.
        """
        pass
