import uuid

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

from .sentences import Sentence
from ..utils.languages import language_choices


def document_directory_path(instance: models.Model, filename:str):
    """
    Where to upload documents

    See https://docs.djangoproject.com/en/5.1/ref/models/fields/#filefield
    """

    return f'documents/{instance.user.id}/{instance.language}/{filename}'


class Document(models.Model):
    """
    Uploaded document with words to study.
    """

    class Meta:
        unique_together = [['user', 'display_name', 'language']]

    id = models.UUIDField(
        primary_key=True,
        blank=True,
        default=uuid.uuid4,
        editable=False,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        help_text=_('User who uploaded this document'),
    )
    display_name = models.CharField(
        max_length=255,
        help_text=_('How the document will be named in the UI'),
    )
    language = models.CharField(
        max_length=8,
        choices=language_choices(),
        help_text=_('Language that the sentence belongs to'),
    )
    doc_file = models.FileField(
        upload_to=document_directory_path,
        unique=True,
    )


class SentenceOrder(models.Model):
    """
    Join table to keep track of sentence order in a document
    """

    class Meta:
        ordering = ['order']
        unique_together = [['sentence', 'document', 'order']]

    sentence = models.ForeignKey(
        Sentence,
        on_delete=models.CASCADE,
    )
    document = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
    )
    order = models.PositiveIntegerField()
