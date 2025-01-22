"""
Copyright (C) J Leadbetter
Affero GPL v3
"""

import json
import os
import pathlib
import uuid

from pydantic import BaseModel


def get_top_level_directory() -> str:
    """
    Gets the top-most level folder of the project.

    :return: absolute path to the project directory.
    """
    project_path = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            '..',
            '..',
        ),
    )
    return project_path


class DatabaseFileMixin:
    """
    Utility functions for file-based databases
    Used with adapter classes
    """

    def _get_db_filename(self, base: str, extension: str):
        """
        Return the absolute path to the database file.
        Assumes file is located in the 'data' directory.

        :base: base file name (e.g., my_database)
        :extension: file extension (e.g., json or sqlite)
        """

        filename = ".".join([
            os.path.join(get_top_level_directory(), 'data', base),
            extension,
        ])
        return filename


class JSONFileMixin:
    """
    Methods for reading and writing to a JSON database file
    Used with adapter classes.

    Must define `self.database`, 
    which is a string for the filename to be read from/written to.
    """

    def _read_json(self) -> 'Database':
        # Import here to avoid recursive import
        from common.models.database import Database

        # Safety precaution: make sure file exists
        pathlib.Path(self.database).touch()

        try:
            with open(self.database, 'r') as input_file:
                data = json.load(input_file) or data
        except json.JSONDecodeError:
            # File is empty; ignore
            return Database()

        return Database.model_validate(data)

    def _write_json(self, data: 'Database'):
        # Import here to avoid recursive import
        from common.models.database import Database

        with open(self.database, 'w') as output_file:
            json.dump(data.model_dump(), output_file, indent=2)
