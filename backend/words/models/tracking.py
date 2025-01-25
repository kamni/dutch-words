import uuid

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

from .words import Conjugation
from ..utils.languages import language_choices


class LearningTracker(models.Model):
    """
    Tracks user progress with conjugations.

    We're not tracking at the word level,
    because we want to ensure that a user has learned all forms of the word.
    """

    class Status(models.TextChoices):
        learned = _('learned')
        currently_learning = _('currently learning')
        waiting_to_learn = _('waiting to learn')
        unknown = _('not conjugated')

    id = models.UUIDField(
        primary_key=True,
        blank=True,
        default=uuid.uuid4,
        editable=False,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        help_text=_('User who is learning this conjugation of a word'),
    )
    # This is on the conjugation,
    # but we're putting this here for normalization
    language = models.CharField(
        max_length=8,
        choices=language_choices(),
        help_text=_('Language that the word belongs to'),
    )
    conjugation = models.ForeignKey(
        Conjugation,
        on_delete=models.CASCADE,
        help_text=_('Word conjugation to learn'),
    )
    status = models.CharField(
        min_length=20,
        choices=Status,
        blank=True,
        default=Status.unknown,
        help_text=_('Current status of user progress'),
    )
