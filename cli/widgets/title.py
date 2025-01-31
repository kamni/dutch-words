"""
Copyright (C) J Leadbetter <j@jleadbetter.com>
Affero GPL v3
"""

import os

from textual.app import ComposeResult
from textual.containers import Center, Container, Horizontal, Vertical, VerticalGroup
from textual.widgets import Static


TITLE_TEXT1 = """
   _   __        __     __     __
 /' )/' _`\\    /' _`\\ /' _`\\ /' _`\\
(_, || ( ) |   | ( ) || ( ) || ( ) |
  | || | | |   | | | || | | || | | |
  | || (_) | _ | (_) || (_) || (_) |
  (_)`\\___/'( )`\\___/'`\\___/'`\\___/'
            |/
"""

TITLE_TEXT2 = """
  _       _                 _
 ( )  _  ( )               ( )
 | | ( ) | |   _    _ __  _| | ___
 | | | | | | /'_`\\ ( '__)'_` /',__)
 | (_/ \\_) |( (_) )| | ( (_| \\__, \\
 `\\___x___/'`\\___/'(_) `\\__,_|____/
"""

SUBTITLE_TEXT = 'Teach yourself 10,000+ words in another language'


class MainTitle(Horizontal):
    """
    Display a main title for 10,000 Words
    """

    CSS_FILE = os.path.join('css', 'title.tcss')

    def compose(self) -> ComposeResult:
        yield Center(
            Center(
                VerticalGroup(
                    Static(TITLE_TEXT1, classes='title-text'),
                    Static(TITLE_TEXT2, classes='title-text'),
                    id='title-text-wrapper',
                ),
                Vertical(
                    Static(SUBTITLE_TEXT, classes='subtitle-text'),
                    id='subtitle-text-wrapper',
                ),
                id='title-wrapper',
            ),
        )
