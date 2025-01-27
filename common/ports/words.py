"""
Copyright (C) J Leadbetter <j@jleadbetter.com>
Affero GPL v3

Interface for retrieving words from storage.
"""

from abc import ABC, abstractmethod
from typing import List

from common.models.words import WordDB


class WordPort(ABC):
    """
    Manages Words in the database
    """

    @abstractmethod
    def create(self, word: WordDB) -> WordDB:
        """
        Create a new word in the database.

        :word: New WordDB object to add to the database.
            Word is counted as a duplicate when it has the same
            languageCode and baseWord.

        :return: Created WordDB object.
        :raises: ObjectExistsError if the object already exists.
        """
        pass

    @abstractmethod
    def create_in_batch(self, words: List[WordDB]) -> List[WordDB]:
        """
        Batch create multiple words.
        Ignores words that already exist.

        :word: New WordDB object to add to the database.
            Word is counted as a duplicate when it has the same
            languageCode and baseWord.

        :return: List of words that were created.
        """
        pass
