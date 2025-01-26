"""
Copyright (C) J Leadbetter <j@jleadbetter.com>
Affero GPL v3
"""

from ..models.documents import DocumentDB, DocumentUIMinimal
from ..ports.documents import DocumentPort
from ..utils.file import JSONFileMixin


class DocumentJSONFileAdapter(JSONFileMixin, DocumentPort):
    """
    Converts documents from a JSON File into UI objects
    """

    def __init__(self, **kwargs):
        self.initialize_database(
            data_dir=kwargs.get('datadir'),
            base_database_name=kwargs.get('databasefile'),
        )

    def read_all_for_user(
        self,
        user_id: str,  # UUID
        language_code: Optional[LanguageCode] = None,
    ) -> List[DocumentUIMinimal]:
        """
        Find documents for the specified user.

        :user_id: User id to search in the database.
        :language_code: optional filter to return documents for a specific
            language. If not specified, returns all documents.

        :return: List of documents
        """

        database = self.read_json()
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



class DocumentAPIAdapter(DocumentPort):
    """
    Converts documents from an HTML API into UI objects
    """

    def read_all_for_user(
        self,
        user_id: str,  # UUID
        language_code: Optional[LanguageCode] = None,
    ) -> List[DocumentUIMinimal]:
        """
        Find documents for the specified user.

        :user_id: User id to search in the database.
        :language_code: optional filter to return documents for a specific
            language. If not specified, returns all documents.

        :return: List of documents
        """
        pass


class DocumentDjangoORMAdapter(DocumentPort):
    """
    Converts documents from the Django ORM into UI objects
    """

    def read_all_for_user(
        self,
        user_id: str,  # UUID
        language_code: Optional[LanguageCode] = None,
    ) -> List[DocumentUIMinimal]:
        """
        Find documents for the specified user.

        :user_id: User id to search in the database.
        :language_code: optional filter to return documents for a specific
            language. If not specified, returns all documents.

        :return: List of documents
        """
        pass
