"""
Copyright (C) J Leadbetter <j@jleadbetter.com>
Affero GPL v3

Implementations of the DatabasePort
"""

import json
import os

from common.models.database import Database
from common.ports.database import DatabaseError, DatabasePort
from common.utils.file import JSONFileMixin


class DatabaseJSONFileAdapter(JSONFileMixin, DatabasePort):
    """
    Stores the database as a JSON file.
    """

    # Implements initialize_database through JSONFileMixin
    def __init__(self, **kwargs):
        self.initialize_database(
            data_dir=kwargs.get('datadir'),
            base_database_name=kwargs.get('databasefile'),
        )

    def teardown_database(self):
        """
        Drop all tables in the database.
        Ignores if database isn't there.

        :raises: DatabaseError if something goes wrong.
        """
        try:
            Path(self._database_file).unlink()
            self._database = {}
        except Exception as ex:
            raise DatabaseError(str(ex))
