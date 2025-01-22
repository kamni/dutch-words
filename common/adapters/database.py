"""
Copyright (C) J Leadbetter <j@jleadbetter.com>
Affero GPL v3

Implementations of the DatabasePort
"""

import json
import os

from common.models.database import Database
from common.ports.database import DatabaseError, DatabasePort
from common.utils.file import DatabaseFileMixin


class DatabaseJSONFileAdapter(DatabaseFileMixin, DatabasePort):
    """
    Stores the database as a JSON file.
    """

    def __init__(self, **kwargs):
        self.database = self._get_db_filename(
            kwargs['databasefile'],
            'json',
        )

    def _write(self, database: Database):
        with open(self.database, 'w') as output_file:
            json.dump(database.model_dump(), output_file, indent=2)

    def initialize_database(self):
        """
        Set up the expected tables in the database.
        Ignores if tables already exist.

        :raises: DatabaseError if something goes wrong.
        """

        try:
            database = Database()
            self._write(database)
        except Exception as ex:
            raise DatabaseError(str(ex))

    def teardown_database(self):
        """
        Drop all tables in the database.
        Ignores if database isn't there.

        :raises: DatabaseError if something goes wrong.
        """
        try:
            if os.path.exists(self.database):
                os.remove(self.database)
        except Exception as ex:
            raise DatabaseError(str(ex))
