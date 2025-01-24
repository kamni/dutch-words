import string

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Document
from .utils.documents import create_sentences_and_words


@receiver(post_save, sender=Document)
def process_document(sender, **kwargs):
    """
    After a document is uploaded, create the sentences and words
    """

    instance = kwargs.get('instance')
    created = kwargs.get('created')
    if instance and created:
        create_sentences_and_words(instance)
