#!/usr/bin/env python3

"""
Copyright (C) J Leadbetter <j@jleadbetter.com>
Affero GPL v3

This script creates a basic json dump that can be used as test data.
"""

import argparse
import csv
import os
import pprint
import sys
from typing import List, Optional, Tuple

TOP_LEVEL_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if TOP_LEVEL_FOLDER not in sys.path:
    sys.path.append(TOP_LEVEL_FOLDER)

from common.models.users import User
from common.models.words import UnknownBase, UnknownDataBase, Word
from common.stores.adapter import AdapterStore

DEFAULT_LANGUAGE_CODE = 'nl'
DEFAULT_FREQUENCIES_FILE = 'parsed_words.txt'
DEFAULT_USERS_FILE = 'users.csv'


class DatabaseCreator:
    def __init__(
        self,
        language_code: str=DEFAULT_LANGUAGE_CODE,
        word_frequencies_file: str=DEFAULT_FREQUENCIES_FILE,
        users_file: str=DEFAULT_USERS_FILE,
        add_default_data: Optional[bool]=False,
    ):
        self.language_code = language_code
        self.frequencies_file = os.path.join(
            TOP_LEVEL_FOLDER,
            'data',
            language_code,
            word_frequencies_file,
        )
        self.users_file = os.path.join(
            TOP_LEVEL_FOLDER,
            'data',
            users_file,
        )
        self.add_default_data = add_default_data

        self.adapter_store = AdapterStore()
        self.adapter_store.initialize()
        self.database_port = self.adapter_store.get('DatabasePort')
        self.user_port = self.adapter_store.get('UserPort')
        self.word_port = self.adapter_store.get('WordPort')

        self.UnknownData = UnknownDataBase(language_code)
        self.Unknown = UnknownBase(
            language_code,
            instantiated_classes=[self.UnknownData],
        )

    def _create_words(self, word_tuples: List[Tuple[str, int]]) -> List[Word]:
        words: List[Word] = []
        for base_word, frequency in word_tuples:
            word = Word(
                frequency=frequency,
                languageCode=self.language_code,
                baseWord=base_word,
                translations=[],
                type=self.Unknown(
                    data=[
                        self.UnknownData(
                            text=base_word,
                        ),
                    ],
                ),
            )
            words.append(word)
        return words

    def _import_users(self) -> List[User]:
        with open(self.users_file) as input_file:
            user_data = [row for row in csv.reader(input_file, delimiter=',')][1:]

        users = [
            User(
                username=user[0],
                display_name=user[1],
                password=user[2],
            )
            for user in user_data
        ]
        return users

    def _import_words(self) -> List[Word]:
        word_data: List[Tuple[str, int]] = []
        with open(self.frequencies_file) as wordfile:
            wordlines = wordfile.readlines()
            for line in wordlines:
                word, frequency = line.split('\t')
                word_data.append((word.strip(), int(frequency.strip())))

        words = self._create_words(word_data)
        return words

    def _write_to_file(self, words: List[Word], users: List[User]):
        self.word_port.create_in_batch(words)
        self.user_port.create_in_batch(users)

    def run(self):
        print('Tearing down and rebuilding database...')
        self.database_port.teardown_database()
        self.database_port.initialize_database()

        if self.add_default_data:
            print('Generating default data...')
            words = self._import_words()
            users = self._import_users()

            print('Writing to database...')
            self._write_to_file(
                words=words,
                users=users,
            )
        else:
            print('Skipping default data.')


        print('Done!')


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser(
        prog='InitializeDatabase',
        description='Initializes database and inserts data from the frequency fiile',
    )
    arg_parser.add_argument(
        '-l',
        '--language-code',
        default=DEFAULT_LANGUAGE_CODE,
        help='Two-letter language code; defaults to "nl"',
    )
    arg_parser.add_argument(
        '-w',
        '--word-frequencies-file',
        default=DEFAULT_FREQUENCIES_FILE,
        help=(
            'Name of the file with defalt word data. '
            'The file must be located in the "data" directory, '
            'in a folder named after the language code '
            '(e.g., "data/nl"). '
            'Ignored if --add-default-data is False.'
        ),
    )
    arg_parser.add_argument(
        '-u',
        '--users-file',
        default=DEFAULT_USERS_FILE,
        help=(
            'Name of the file with default user data. '
            'The file must be located in the root of the "data" directory. '
            'Ignored if --add-default-data is False.'
        ),
    )
    arg_parser.add_argument(
        '-d',
        '--add-default-data',
        action='store_true',
        default=False,
    )
    arg_parser.add_argument(
        '--force',
        default=False,
        action='store_true',
        help=('Force destruction of the database; do not prompt for confirmation.'),
    )
    args = arg_parser.parse_args()

    if not args.force:
        print('WARNING: This will destroy the existing database, if it exists!!!')
        while True:
            confirm_database_teardown = input('Are you sure you want to do this? (yes/no) ')
            response = confirm_database_teardown.lower()
            if response not in ['yes', 'no']:
                print('Please type "yes" or "no"')
                continue
            elif response == 'no':
                print('Aborting.')
                sys.exit(0)
            else:
                break

    DatabaseCreator(
        language_code=args.language_code,
        word_frequencies_file=args.word_frequencies_file,
        users_file=args.users_file,
        add_default_data=args.add_default_data,
    ).run()
