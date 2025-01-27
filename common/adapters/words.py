"""
Copyright (C) J Leadbetter <j@jleadbetter.com>
Affero GPL v3

Implementations of WordPort for retrieving words from storage.
"""

import json
import os
import pathlib
from typing import Dict, List, Optional

from common.models.words import WordDB
from common.ports.words import WordPort
from common.utils.file import JSONFileMixin


class WordJSONFileAdapter(JSONFileMixin, WordPort):
    """
    Handler for JSON file database.

    WARNING: This is only intended for local development.
    Do not use in production environments.
    """

    def __init__(self, **kwargs):
        self.initialize_database(
            data_dir=kwargs.get('datadir'),
            base_database_name=kwargs.get('databasefile'),
        )

    def _is_duplicate(
        self,
        existing_words: List[WordDB],
        new_word: List[WordDB],
    ) -> bool:
        return new_word in existing_words

    def create(self, word: WordDB) -> WordDB:
        """
        Create a new word in the database.

        :word: New WordDB object to add to the database.
            Word is counted as a duplicate when it has the same
            languageCode and baseWord.

        :return: Created WordDB object.
        :raises: ObjectExistsError if the object already exists.
        """

        database = self._read_json()

        if self._is_duplicate(database.words, word):
            raise ObjectExistsError(
                f'Word with {word.baseWord} already exists for "{word.languageCode}"')

        word.set_id()
        database.words.append(word)
        self._write_json(database)
        return word

    def create_in_batch(self, words: List[WordDB]) -> List[WordDB]:
        """
        Batch create multiple words.
        Ignores words that already exist.

        :word: New WordDB object to add to the database.
            Word is counted as a duplicate when it has the same
            languageCode and baseWord.

        :return: List of words that were created.
        """
        database = self._read_json()
        non_duplicates = list(set(words).difference(set(database.words)))
        if non_duplicates:
            for word in non_duplicates:
                word.set_id()
            database.words.extend(non_duplicates)
            self._write_json(database)
        return non_duplicates
