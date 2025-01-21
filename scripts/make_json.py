#!/usr/bin/env python3

"""
Copyright (C) J Leadbetter <j@jleadbetter.com>
Affero GPL v3

This script creates a basic json dump that can be used as test data.
"""

import argparse
import os
import pprint
import sys
from typing import List, Tuple

from pydantic import BaseModel

TOP_LEVEL_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(TOP_LEVEL_FOLDER)

from common.adapters.words import WordJSONFileAdapter
from common.models.words import UnknownDataBase, UnknownBase, Word

DEFAULT_LANGUAGE_CODE = 'nl'
DEFAULT_FREQUENCIES_FILE = 'parsed_words.txt'
DEFAULT_OUTPUT_FILE = 'database.json'


class JSONCreator:
    def __init__(
        self,
        language_code: str=DEFAULT_LANGUAGE_CODE,
        frequencies_file: str=DEFAULT_FREQUENCIES_FILE,
        output_file: str=DEFAULT_OUTPUT_FILE,
    ):
        self.language_code = language_code
        self.frequencies_file = os.path.join(
            TOP_LEVEL_FOLDER,
            'data',
            language_code,
            frequencies_file,
        )
        self.output_file = os.path.join(
            TOP_LEVEL_FOLDER,
            'data',
            output_file,
        )

        self.word_port = WordJSONFileAdapter(self.output_file)

        self.word_classes = {}
        self.word_classes['UnknownData'] = UnknownDataBase(language_code)
        self.word_classes['Unknown'] = UnknownBase(
            language_code,
            instantiated_classes=self.word_classes,
        )

    def _create_words(self, word_tuples: List[Tuple[str, int]]) -> List[Word]:
        words: List[Word] = []
        for base_word, frequency in word_tuples:
            word = Word(
                frequency=frequency,
                languageCode=self.language_code,
                baseWord=base_word,
                translations=[],
                type=self.word_classes['Unknown'](
                    type='unknown',
                    data=[
                        self.word_classes['UnknownData'](
                            text=base_word,
                        ),
                    ],
                ),
            )
            words.append(word)
        return words

    def _import_words(self) -> List[Tuple[str, int]]:
        words: List[Tuple[str, int]] = []
        with open(self.frequencies_file) as wordfile:
            wordlines = wordfile.readlines()
            for line in wordlines:
                word, frequency = line.split('\t')
                words.append((word.strip(), int(frequency.strip())))
        return words

    def _write_to_file(self, words: List[Word]):
        self.word_port.create_words(words)

    def run(self):
        words = self._import_words()
        database_words = self._create_words(words)
        self._write_to_file(database_words)


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser(
        prog='MakeJSON',
        description='Turns parsed word frequencies into minimal JSON',
    )
    arg_parser.add_argument(
        '-l',
        '--language-code',
        default=DEFAULT_LANGUAGE_CODE,
        help='Two-letter language code; defaults to "nl"',
    )
    arg_parser.add_argument(
        '-f',
        '--frequencies-file',
        default=DEFAULT_FREQUENCIES_FILE,
        help=(
            'Name of the file that will be parsed by the script. '
            'The file must be located in the data folder, '
            'in a folder named after the language code.'
        ),
    )
    arg_parser.add_argument(
        '-o',
        '--output-file',
        default=DEFAULT_OUTPUT_FILE,
        help=(
            'Name of the file that will store the parsed output. ',
            'The file will be located in the data folder, '
            'in a folder named after the language code.'
        ),
    )
    args = arg_parser.parse_args()
    JSONCreator(
        language_code=args.language_code,
        frequencies_file=args.frequencies_file,
        output_file=args.output_file,
    ).run()
