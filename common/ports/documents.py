"""
Copyright (C) J Leadbetter <j@jleadbetter.com>
Affero GPL v3
"""

from abc import ABC, abstractmethod
from typing import List, Optional

from ..models.documents import DocumentDB
from ..utils.languages import LanguageCode


class DocumentPort(ABC):
    """
    Manages Documents in the database, UI, and API
    """

    @abstractmethod
    def get_all(
        self,
        user_id: str,  # UUID
        language_code: Optional[LanguageCode] = None,
    ) -> List[DocumentDB]:
        """
        Find all documents for the specified user.

        :user_id: User id to search in the database.
        :language_code: optional filter to return documents for a specific
            language. If not specified, returns all documents.

        :return: List of documents
        """
        pass
