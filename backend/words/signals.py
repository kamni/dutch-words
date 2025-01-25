import string

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Conjugation, Document
from .utils.documents import create_sentences_and_words


@receiver(post_save, sender=Document)
def process_document(sender, **kwargs):
    """
    After a document is uploaded, create the Sentences and Words
    """

    instance = kwargs.get('instance')
    created = kwargs.get('created')
    if instance and created:
        create_sentences_and_words(instance)


@receiver(post_save, sender=Conjugation)
def create_tracker(sender, **kwargs):
    """
    After a Conjugation is created, create a new LearningTracker
    """

    instance = kwargs.get('instance')
    created = kwargs.get('created')
    if instance and created:
        Conjugation.objects.create(
            user=instance.user,
            language=instance.language,
            conjugation=instance,
        )
