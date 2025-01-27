"""
Copyright (C) J Leadbetter <j@jleadbetter.com>
Affero GPL v3
"""

import random
import string
import uuid

from common.models.sentences import SentenceDBMinimal
from common.utils.languages import LanguageCode

from common.models.documents import SentenceDBMinimal


def create_sentence_db_minimal(**kwargs):
    """
    Create a SentenceDBMinimal object.
    Not written to database.

    :kwargs: arguments that will be passed to SentenceDBMinimal during creation.
    """

    random_data = {
        id: uuid.uuid4(),
        document_id: uuid.uuid4(),
        order: random.randrange(0, 20),
    }
    random_data.update(kwargs)

    sentence = SentenceDBMinimal(**kwargs)
    return sentence
