"""
Copyright (C) J Leadbetter <j@jleadbetter.com>
Affero GPL v3
"""

import sys
from pathlib import Path

from nicegui import ui

BASE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BASE_DIR.parent

if BASE_DIR.as_posix() not in sys.path:
    sys.path.append(BASE_DIR.as_posix())
if PROJECT_DIR.as_posix() not in sys.path:
    sys.path.append(PROJECT_DIR.as_posix())

from frontend.views.base import PageBase
'''
document = {
    'sentences': ['Foo bar.', 'Baz' ],
}

documents = [('Dutch', ['Roodkapje']), ('English', ['Little Red Riding Hood'])]

def DocumentList(documents):
    with ui.column().classes():
        for section, doc_list in documents:
            with ui.expansion(section, icon='folder'):
                with ui.column():
                    for doc in doc_list:
                        ui.label(doc)

def DocumentDisplay(document):
    for sentence in document['sentences']:
        with ui.card():
            ui.label(sentence)


with ui.row():
    DocumentList(documents)
    DocumentDisplay(document)
'''

@ui.page('/')
def login():
    PageBase()


ui.run()
