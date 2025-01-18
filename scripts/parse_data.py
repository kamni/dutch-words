#!/usr/bin/env python3

"""
Copyright (C) J Leadbetter <j@jleadbetter.com>
GNU GPL v3

This script parses the data from the Universität Leipzig Corpora Collection for
Dutch, which has a separate copyright from this script (CC BY-NC).
"""

import os
import string
from typing import Dict, List, Tuple

TOP_LEVEL_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATA_FILENAME = 'nld_mixed-typical_2012_1M-words.txt'
DATA_FILE = os.path.join(TOP_LEVEL_FOLDER, 'data', DATA_FILENAME)
OUTPUT_FILENAME = 'top-10000-dutch-words.txt'
OUTPUT_FILE = os.path.join(TOP_LEVEL_FOLDER, OUTPUT_FILENAME)


class Parser:
    def __init__(self, input_file: str=DATA_FILE, output_file: str=OUTPUT_FILE):
        self.input_file = input_file
        self.output_file = output_file

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
        words = dict(sorted(tmp_words, key=lambda x: x[1], reverse=True)[:10000]).keys()
        wordlines = [f'{word}\n' for word in words]
        return wordlines

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

    def _write_to_file(self, words: List[str]):
        with open(self.output_file, 'w') as wordfile:
            wordfile.writelines(words)

    def run(self):
        words = self._import_words()
        self._write_to_file(words)


if __name__ == '__main__':
    Parser().run()
