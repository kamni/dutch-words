"""
Copyright (C) J Leadbetter <j@jleadbetter.com>
Affero GPL v3
"""

from frontend.views.base import BaseView


class ConfigureView(BaseView):
    """
    Configure the app.

    This view has two modes.
    The first time the app is configured, no login is necessary.
    However, subsequent access requires an admin user.
    """
    pass
