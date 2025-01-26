"""
Copyright (C) J Leadbetter <j@jleadbetter.com>
Affero GPL v3
"""

from pydantic import BaseModel


class DocumentDB(BaseModel):
    """
    Representation of a document in the database
    """
    pass


class DocumentUIMinimal(BaseModel):
    """
    Bare minimum display of documents in the UI
    Excludes Sentences and Words
    """
    pass


class DocumentUIFull(BaseModel):
    """
    All information needed to display a Document and its Sentences/Words.
    Includes user tracking for learned words
    """
    pass
