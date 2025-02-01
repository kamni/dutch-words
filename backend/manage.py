#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""

import os
import sys
import warnings
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parent.parent.parent
if PROJECT_DIR.as_posix() not in sys.path:
    sys.path.append(PROJECT_DIR.as_posix())


def main():
    """Run administrative tasks."""
    # Custom code to run multiple servers
    try:
        requires_postgres = sys.argv.pop(sys.argv.index('--requires-postgres'))
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings_postgres')
    except ValueError:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
