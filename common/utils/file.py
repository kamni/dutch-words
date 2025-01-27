"""
Copyright (C) J Leadbetter
Affero GPL v3
"""

import json
from pathlib import Path
from typing import Optional

from pydantic import BaseModel

from ..models.database import Database


BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = 'data'


class JSONFileMixin:
    """
    Methods for reading and writing to a JSON database file
    Used with adapter classes.

    Call `self.initialize_db` in the init.
    """

    _database = None

    def initialize_database(
        self,
        data_dir: Optional[str]=None,
        base_database_name: Optional[str]=None,
    ):
        """
        Set up the JSON database for the class.
        Database as a Database object can be accessed through self._database

        :data_dir: Location of the directory where the database will be saved.
            Default is '/data' relative to the project folder.
        :base_database_name: What the file should be called.
            Example: 'database' will create a file called 'database.json'.
            Default is 'database'.
        """

        base_database_name = base_database_name or 'database'
        data_dir = data_dir or DATA_DIR
        self._database_file = BASE_DIR / data_dir / f'{base_database_name}.json'
        self.read_db()

    @property
    def database_file(self):
        return self._database_file

    def read_db(self, force_reread=False) -> Database:
        """
        Get the Database representation of the json database file.
        To save on file reads, returns data from self._database
        if it already exists.

        :force_reread: Don't return existing data from self._database;
            instead, re-initialize self._database.
        """

        if self._database and not force_reread:
            return self._database

        # Ensure the file exists
        Path(self.database_file).touch(exist_ok=True)

        database = Database()
        try:
            with open(self.database_file, 'r') as input_file:
                data = json.load(input_file) or data

            database = Database.model_validate(data)
        except json.JSONDecodeError:
            # File is empty; ignore
            pass

        self._database = database
        return self._database

    def write_db(self, database: Optional[Database]=None):
        """
        Write self._database to the json file.

        :database: If supplied, overwrites the existing self._database
            before writing to file
        """
        if database:
            self._database = database

        with open(self._database_file, 'w') as output_file:
            json.dump(self._database.model_dump(), output_file, indent=2)
