"""
Copyright (C) J Leadbetter <j@jleadbetter.com>
Affero GPL v3
"""

import os
import sys
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
if not PROJECT_DIR.as_posix() in sys.path:
    sys.path.append(PROJECT_DIR.as_posix())

BACKEND_DIR = PROJECT_DIR / 'backend'
if not BACKEND_DIR.as_posix() in sys.path:
    sys.path.append(BACKEND_DIR.as_posix())

from .app import TenThousandWordsApp


app = TenThousandWordsApp()
app.run()
