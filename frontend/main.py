"""
Copyright (C) J Leadbetter <j@jleadbetter.com>
Affero GPL v3
"""

import sys
from pathlib import Path

from nicegui import app, ui
from nicegui.storage import set_storage_secret

BASE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BASE_DIR.parent

if BASE_DIR.as_posix() not in sys.path:
    sys.path.append(BASE_DIR.as_posix())
if PROJECT_DIR.as_posix() not in sys.path:
    sys.path.append(PROJECT_DIR.as_posix())

from frontend.middleware.auth import AuthMiddleware
from frontend.views.base import BaseView


UNSAFE_SECRET_KEY = 'UNSAFE_jsn9wx-vje-+#k%(b*kra1std2^v43^jtq&)5x26whm'

app.add_middleware(AuthMiddleware)


@ui.page('/')
def login():
    view = BaseView()
    return view.display()


@ui.page('/edit')
def edit():
    ui.label('edit page')


if __name__ in {'__main__', '__mp_main__'}:
    ui.run()
    set_storage_secret(UNSAFE_SECRET_KEY)
