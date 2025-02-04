"""
Copyright (C) J Leadbetter <j@jleadbetter.com>
Affero GPL v3
"""

from fastapi import Request
from fastapi.responses import RedirectResponse
from nicegui import app
from starlette.middleware.base import BaseHTTPMiddleware


UNRESTRICTED_PAGE_ROUTES = {'/'}


class AuthMiddleware(BaseHTTPMiddleware):
    """
    Restricts access to other pages in the app.

    Modified from:
    https://github.com/zauberzeug/nicegui/tree/main/examples/authentication/main.py
    """

    async def dispatch(self, request: Request, call_next):
        if not app.storage.user.get('authenticated', False):
            if request.url.path not in UNRESTRICTED_PAGE_ROUTES:
                # Remember where the user wanted to go
                app.storage.user['referrer_path'] = request.url.path
                return RedirectResponse('/')
        return await call_next(request)
