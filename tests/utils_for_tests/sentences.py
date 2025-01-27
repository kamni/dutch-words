"""
Copyright (C) J Leadbetter <j@jleadbetter.com>
Affero GPL v3
"""

import random
import string

from common.models.sentences import SentenceDBMinimal
from common.utils.languages import LanguageCode

from .random_data import random_uuid

def create_sentence_db_minimal(**kwargs):
    """
    Create a SentenceDBMinimal object.
    Not written to database.

    :kwargs: arguments that will be passed to SentenceDBMinimal during creation.
    """

    random_data = {
        'id': random_uuid(),
        'document_id': random_uuid(),
        'order': random.randrange(0, 20),
    }
    random_data.update(kwargs)

    sentence = SentenceDBMinimal(**random_data)
    return sentence
