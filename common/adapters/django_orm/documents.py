"""
Copyright (C) J Leadbetter <j@jleadbetter.com>
Affero GPL v3
"""

from typing import List

from ...ports.documents import DocumentDBPort, DocumentUIPort


class DocumentDBDjangoORMPort(DocumentDBPort):
    """
    Represents a document in the system
    """

    def create(self, document: DocumentDB) -> DocumentDB:
        """
        Create a document in the database.

        :document: Instance of a DocumentDB to save

        :return: DocumentDB that was created
        :raises: ObjectExistsError when document with the same user
            and file_path exists
        """
        pass

    def get(self, id: uuid.UUID, user_id: uuid.UUID) -> DocumentDB:
        """
        Get the specified document by id.

        :id: The id of the document
        :user_id: The user's id that owns the document

        :return: DocumentDB matching the id.
        :raises: ObjectNotFoundError if no matching document is found
            for the user
        """
        pass

    def get_all(self, user_id: uuid.UUID) -> List[DocumentDB]:
        """
        Get all documents for the specified user.

        :user_id: The user's id who owns the documents

        :return: List of documents (may be empty)
        """
        pass


class DocumentUIDjangoORMPort(DocumentUIPort):
    """
    Represents documents to the UI
    """

    def get(self, document: DocumentDB) -> DocumentUI:
        """
        Gets a full representation of the document,
        including child sentences and conjugations.

        :document: Database representation of the document.

        :return: Document instance ready for display in the UI.
        """
        pass

    def get_all_minimal(
        self,
        documents: List[DocumentDB],
    ) -> List[DocumentUIMinimal]:
        """
        Convert a list of database documents into a list of minimal UI objects.

        :documents: DocumentDB instances.
        :return: List of DocumentUIMinimal objects.
        """
        pass
