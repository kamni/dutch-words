"""
Copyright (C) J Leadbetter <j@jleadbetter.com>
Affero GPL v3
"""

from typing import List, Optional

from ..models.documents import DocumentDB
from ..ports.documents import DocumentPort
from ..utils.file import JSONFileMixin
from ..utils.languages import LanguageCode


class DocumentJSONFileAdapter(JSONFileMixin, DocumentPort):
    """
    Converts documents from a JSON File into UI objects
    """

    def __init__(self, **kwargs):
        self.initialize_database(
            data_dir=kwargs.get('datadir'),
            base_database_name=kwargs.get('databasefile'),
        )

    def get_all(
        self,
        user_id: str,  # UUID
        language_code: Optional[LanguageCode] = None,
    ) -> List[DocumentDB]:
        """
        Find documents for the specified user.

        :user_id: User id to search in the database.
        :language_code: optional filter to return documents for a specific
            language. If not specified, returns all documents.

        :return: List of documents
        """

        database = self.read_db()
        try:
            user = list(filter(
                lambda x: x.id == user_id,
                database.users,
            ))[0]
        except IndexError:
            # If user isn't found, return an empty list.
            # We don't want to inform hackers that a user doesn't exist.
            return []

        documents = filter(
            lambda x: x.user_id == user_id,
            database.documents,
        )
        if language_code:
            documents = filter(
                lambda x: x.language_code == language_code,
                documents,
            )

        return list(documents)
