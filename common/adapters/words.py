"""
Copyright (C) J Leadbetter <j@jleadbetter.com>
Affero GPL v3
"""

import json
import pathlib
from enum import Enum
from typing import Dict, List, Optional

from common.models.database import Database
from common.models.words import Word
from common.ports.words import WordPort


class WordJSONFileAdapter(WordPort):
    """
    Writes the Word objects as JSON to a file.

    WARNING: This is not thread safe and should only be used for development.
    """

    def __init__(self, input_file: str, output_file: Optional[str]=None):
        self.input_file = input_file
        # The same file can be read and written back to
        self.output_file = output_file or input_file

    def _is_duplicate(
        self,
        existing_words: List[Word],
        new_word: List[Word],
    ) -> bool:
        return new_word in existing_words

    def _read_json(self) -> Database:
        # Safety precaution: make sure file exists
        pathlib.Path(self.input_file).touch()

        data = {'words': []}
        try:
            with open(self.input_file, 'r') as input_file:
                data = json.load(input_file) or data
        except json.JSONDecodeError:
            # File is empty; ignore
            pass

        return Database.model_validate(data)

    def _write_json(self, data: Database):
        with open(self.output_file, 'w') as output_file:
            json.dump(data.model_dump(), output_file, indent=2)

    def create_word(self, word: Word) -> Word:
        """
        Create a new word in the database.

        :word: New Word object to add to the database.
            Word is counted as a duplicate when it has the same
            languageCode and baseWord.

        :return: Created Word object.
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

    def create_words(self, words: List[Word]) -> List[Word]:
        """
        Batch create multiple words.
        Ignores words that already exist.

        :word: New Word object to add to the database.
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

    def create_or_update_word(self, word: Word) -> Word:
        """
        Create a new word, or update an existing word in the database.

        :word: New Word object to add to the database.
            Word is counted as a duplicate when it has the same
            languageCode and baseWord.

        :return: Created Word object.
        """
        raise NotImplementedError()

    def read_word(self, language_code: str, base_word: str) -> Word:
        """
        Retrieve a word from the database.

        :language_code: 2-letter language code of the Word.
        :base_word: Base word (non-conjugated) of the Word.

        :return: Word object, if it exists.
        :raises: ObjectNotFoundError
        """
        raise NotImplementedError()

    def read_words(self, number: int=100, offset: int=0) -> List[Word]:
        """
        Retrieve multiple words from the database.

        :number: Return a specified number of entries from the database.
        :offset: Where in the database to start the retrieval.

        :return: list of Word objects
        """
        raise NotImplementedError()

    def update_word(self, word: Word) -> Word:
        """
        Update an existing word in the database.

        :word: Word object to update.
            Words are considered the same when they have the same
            languageCode and baseWord.

        :return: Updated Word object.
        :raises: ObjectNotFoundError if Word isn't already in the database.
            Use `create_or_update` if you're not sure the Word exists.
        """
        raise NotImplementedError()

    def delete_word(self, word: Word) -> bool:
        """
        Remove an existing word in the database.

        :word: Word object to delete.
            Words are considered the same when they have the same
            languageCode and baseWord.

        :return: boolean -- true if deleted, false if Word does not exist.
            No errors should be thrown if the Word doesn't exist.
        """
        raise NotImplementedError()

    def merge_word(self, word: Word) -> Word:
        """
        Search the database for baseWords matching the text in WordData.
        Merge those Words into the current Word and remove old words.
        This is especially useful when fixing words that were previously
        imported as 'unknown' type.

        :word: Word to be merged.
            Should safely handle if Words do not exist, or if the list is empty.

        :return: New/updated Word.
        """
        raise NotImplementedError()
