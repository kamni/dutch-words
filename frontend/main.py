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
from frontend.views.configure import ConfigureView
from frontend.views.login import LoginView


UNSAFE_SECRET_KEY = 'UNSAFE_jsn9wx-vje-+#k%(b*kra1std2^v43^jtq&)5x26whm'

#app.add_middleware(AuthMiddleware)


@ui.page('/')
async def login():
    ui.page_title('Login')
    view = LoginView()
    return await view.display()


@ui.page('/configure')
async def configure():
    ui.page_title('Configure Settings')
    view = ConfigureView()
    return await view.display()


@ui.page('/edit')
def edit():
    ui.page_title('Editing Mode')
    ui.label('edit page')


if __name__ in {'__main__', '__mp_main__'}:
    ui.run(favicon='💬')
    set_storage_secret(UNSAFE_SECRET_KEY)
