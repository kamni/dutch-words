"""
Copyright (C) J Leadbetter <j@jleadbetter.com>
Affero GPL v3
"""

from abc import ABC, abstractmethod

from ..models.documents import DocumentUIMinimal
from ..models.users import UserUI
from ..utils.languages import LanguageCode


class DocumentPort(ABC):
    """
    Manages Documents in the database, UI, and API
    """

    @abstractmethod
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
