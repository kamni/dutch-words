"""
Copyright (C) J Leadbetter <j@jleadbetter.com>
Affero GPL v3
"""

from common.models.documents import DocumentUIMinimal
from common.ports.documents import DocumentPort
from common.utils.languages import LanguageCode

from ..models.documents import Document


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

        documents = Document.objects.filter(user__id=user_id)
        if language_code:
            pass

