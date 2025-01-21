#!/usr/bin/env python3

"""
Copyright (C) J Leadbetter <j@jleadbetter.com>
Affero GPL v3

This script parses the data from the Universität Leipzig Corpora Collections.
The data has a separate copyright from this script (CC-BY-NC).
"""

import argparse
import os
import string
from typing import Dict, List, Tuple

TOP_LEVEL_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DEFAULT_MINIMUM_FREQUENCY = 8
DEFAULT_LANGUAGE_CODE = 'nl'
DEFAULT_INPUT_FILE = 'corpora_collection.txt'
DEFAULT_OUTPUT_FILE = 'parsed_words.txt'


class Parser:
    def __init__(
        self,
        minimum_frequency: int=DEFAULT_MINIMUM_FREQUENCY,
        language_code: str=DEFAULT_LANGUAGE_CODE,
        input_file: str=DEFAULT_OUTPUT_FILE,
        output_file: str=DEFAULT_INPUT_FILE,
    ):
        self.minimum_frequency = minimum_frequency
        self.input_file = os.path.join(
            TOP_LEVEL_FOLDER,
            'data',
            language_code,
            input_file,
        )
        self.output_file = os.path.join(
            TOP_LEVEL_FOLDER,
            'data', 
            language_code,
            output_file,
        )

    def _clean_word(self, word_line: List[str]) -> Tuple[str, int]:
        tmp_word, tmp_count = word_line.split('\t')[1:3]

        no_whitespace = tmp_word.strip()
        # We're only removing punctuation on the ends,
        # because Dutch uses an apostrophe for some plurals,
        # which should be kept.
        no_punctuation = no_whitespace.strip(string.punctuation)
        no_digits = no_punctuation.strip(string.digits)
        no_symbols = self._remove_symbols(no_digits)
        word = no_symbols.lower()

        count = int(tmp_count.strip())
        return word, count

    def _import_words(self) -> List[str]:
        imported_words = self._read_file()
        tmp_words = [(key, value) for key, value in imported_words.items()]
        sorted_words = sorted(
            tmp_words,
            key=lambda x: x[1],
            reverse=True,
        )
        if self.minimum_frequency > 0:
            words = list(
                filter(lambda x: x[1] >= self.minimum_frequency, sorted_words),
            )
        else:
            words = sorted_words
        return words

    def _read_file(self) -> Dict[str, int]:
        with open(self.input_file) as wordfile:
            raw_word_data = wordfile.readlines()
            words = {}
            for line in raw_word_data:
                tmp_word, count = self._clean_word(line)
                if tmp_word:
                    word = tmp_word.lower()
                    if word in words:
                        words[word] = words[word] + count
                    else:
                        words[word] = count
        return words

    def _remove_symbols(self, word: str) -> str:
        if not word.isalpha() or len(word) < 2:
            return ''
        return word

    def _write_to_file(self, words: List[Tuple[str, int]]):
        wordlines = [f'{word}\t{count}\n' for word, count in words]
        with open(self.output_file, 'w') as wordfile:
            wordfile.writelines(wordlines)

    def run(self):
        words = self._import_words()
        self._write_to_file(words)


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser(
        prog='ParseData',
        description='Parses word lists from the Universität Leipzig Corpora Collections')
    arg_parser.add_argument(
        '-m',
        '--minimum-frequency',
        type=int,
        default=DEFAULT_MINIMUM_FREQUENCY,
        help=(
            'Cutoff for frequency of words; defaults to 8. '
            'If -1 is specified, return all.'
        ),
    )
    arg_parser.add_argument(
        '-l',
        '--language-code',
        default=DEFAULT_LANGUAGE_CODE,
        help='Two-letter language code; defaults to "nl"',
    )
    arg_parser.add_argument(
        '-i',
        '--input-file',
        default=DEFAULT_INPUT_FILE,
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
    Parser(
        minimum_frequency=args.minimum_frequency,
        language_code=args.language_code,
        input_file=args.input_file,
        output_file=args.output_file,
    ).run()
