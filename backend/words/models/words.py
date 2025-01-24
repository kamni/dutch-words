import uuid

from django.contrib.auth.models import User
from django.db import Q, models
from django.utils.translation import gettext_lazy as _

from .language_codes import language_choices


def word_directory_path(instance: models.Model, filename:str):
    """
    Where to upload audio files for words

    See https://docs.djangoproject.com/en/5.1/ref/models/fields/#filefield
    """

    return f'audio/{instance.user.id}/{instance.language}/{filename}'


class Word(models.Model):
    """
    Word imported from a Document by a User.
    """

    class PartOfSpeechType(models.TextChoices):
        """
        Grammatical part of speech.

        NOTES:

        * Articles are not included here.
          They should be included as part of a noun.

        * Prepositions are not included here,
          because they don't translate well between languages.
          They should be paired with either a verb or an expression.

        * Expressions are for multiple words that mean something different
          than their individual words, and are normally learned together.
          Examples: 'Merry Christmas' and 'It's raining cats and dogs'

        * The 'unknown' type is used for newly imported words,
          until the user sets the type.
        """

        unknown = 'unknown'
        noun = 'noun'
        pronoun = 'pronoun'
        adjective = 'adjective'
        adverb = 'adverb'
        verb = 'verb'
        participle = 'participle'
        conjunction = 'conjunction'
        expression = 'expression'

    class Meta:
        unique_together=[('user', 'language', 'root_word')]

    id = models.UUIDField(
        primary_key=True,
        blank=True,
        default=uuid.uuid4,
        editable=False,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        help_text=_('User who uploaded this word'),
    )
    language = models.CharField(
        max_length=3,
        choices=language_choices(),
        help_text=_('Language that the word belongs to'),
    )
    type = models.CharField(
        max_length=20,
        choices=PartOfSpeechType,
        help_text=_(
            'The word type, i.e., the grammatical part of speech. '
            'Articles and prepositions should be added to either a noun, '
            'verb, or expression, because they rarely make sense on their '
            'own.'
        ),
    )
    root_word = models.CharField(
        max_length=100,
        help_text=_('The base root word in the language'),
    )
    audio_file = models.FileField(
        upload_to=word_directory_path,
        blank=True,
        null=True,
    )
    translations = models.ManyToMany(
        'self',
        symmetrical=True,
        help_text=_('Words in other language that mean the same or similar'),
    )


class Conjugation(models.Model):
    """
    Variation of a word.
    Depending on the language, not all fields are necessary.

    Example: In English, words like 'apple' don't have gender.
    But it does have a plural ('apples'),
    and uses 'an' for singular,
    and 'the' for both singular and plural.
    """

    class Case(models.TextChoices):
        nominative = 'nominative'
        accusative = 'accusative'
        dative = 'dative'
        genitive = 'genitive'

    class Person(models.TextChoices):
        first = 'first'
        second = 'second'
        third = 'third'

    class Plurality(models.TextChoices):
        single = 'single'
        plural = 'plural'

    class Gender(models.TextChoices):
        neutral = 'neutral'
        feminine = 'feminine'
        masculine = 'masculine'

    class Politeness(models.TextChoices):
        casual = 'casual'
        formal = 'formal'

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
        help_text=_('User who uploaded this conjugation'),
    )
    word = models.ForeignKey(
        Word,
        on_delete=models.CASCADE,
    )
    text = models.CharField(
        max_length=255,
    )
    audio_file = models.FileField(
        upload_to=word_directory_path,
        blank=True,
        null=True,
    )
    article = models.CharField(
        max_length=40,
        blank=True,
        null=True,
    )
    case = models.CharField(
        max_length=40,
        blank=True,
        null=True,
        choices=Case,
    )
    gender = models.CharField(
        max_length=40,
        blank=True,
        null=True,
        choices=Gender,
    )
    plurality = models.CharField(
        max_length=40,
        blank=True,
        null=True,
        choices=Plurality,
    )
    politeness = models.CharField(
        max_length=40,
        blank=True,
        null=True,
        choices=Politeness,
    )
    tense = models.CharField(
        max_length=40,
        blank=True,
        null=True,
    )
    audio_file = models.FileField(
        upload_to=word_directory_path,
        blank=True,
        null=True,
    )
