import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

from .language_codes import language_choices
from .words import Word


def sentence_directory_path(instance: models.Model, filename:str):
    """
    Where to upload audio files for whole sentences

    See https://docs.djangoproject.com/en/5.1/ref/models/fields/#filefield
    """

    return f'audio/{instance.user.id}/{instance.language}/{filename}'


class Sentence(models.Model):
    """
    Sentence from an uploaded document.
    """

    class Meta:
        unique_together = [['user', 'language', 'text']]

    id = models.UUIDField(
        primary_key=True,
        blank=True,
        default=uuid.uuid4,
        editable=False,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        help_text=_('User who uploaded this sentence'),
    )
    language = models.CharField(
        max_length=3,
        choices=language_choices(),
        help_text=_('Language that the sentence belongs to'),
    )
    text = models.TextField()
    audio_file = models.FileField(
        upload_to=sentence_directory_path,
        blank=True,
        null=True,
    )
    translations = models.ManyToMany(
        'self',
        symmetrical=True,
        help_text=_('Sentences in other language that mean the same or similar'),
    )


class WordOrder(models.Model):
    """
    Join table to keep track of word order in a sentence
    """

    class Meta:
        ordering = ['order']
        unique_together = [['word', 'sentence', 'order']]

    word = models.ForeignKey(
        Word,
        on_delete=models.CASCADE,
    )
    sentence = models.ForeignKey(
        Sentence,
        on_delete=models.CASCADE,
    )
    order = models.PositiveIntegerField()
