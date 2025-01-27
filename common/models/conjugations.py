"""
Copyright (C) J Leadbetter <j@jleadbetter.com>
Affero GPL v3

NOTE: A 'conjugation' in this context is a variation on a root word.
For example, the English verb 'to go' has multiple conjugations.
such as 'went', 'goes', 'will have gone'.
"""

from enum import StrEnum
from typing import List, Optional

from pydantic import BaseModel

from .base import HashableDBMixin
from .tracking import ProgressTrackerUI
from .users import UserUI
from ..utils.languages import LanguageCode


class Case(StrEnum):
    nominative = 'nominative'
    accusative = 'accusative'
    dative = 'dative'
    genitive = 'genitive'


class Person(StrEnum):
    first = 'first'
    second = 'second'
    third = 'third'


class Plurality(StrEnum):
    single = 'single'
    plural = 'plural'


class Gender(StrEnum):
    neutral = 'neutral'
    feminine = 'feminine'
    masculine = 'masculine'


class Politeness(StrEnum):
    casual = 'casual'
    formal = 'formal'


class Emphasis(StrEnum):
    stressed = 'stressed'
    unstressed = 'unstressed'


class ConjugationDBMinimal(HashableDBMixin, BaseModel):
    """
    Minimal representation of a conjugation stored in the database
    """

    id: str  # UUID
    sentence_id: str  # UUID
    tracking_id: str  # UUID
    order: int  # Relative to the SentenceDB

    @property
    def unique_fields(self):
        return ['id', 'sentence_id', 'order']


class ConjugationDB(HashableDBMixin, BaseModel):
    """
    Representation of a conjugation in the Database.
    """

    id: Optional[str] = None  # UUID. Set by the database.
    user_id: str  # UUID.
    tracking_id: Optional[str]  # UUID
    order: int  # Relative to SentenceDB
    language_code: LanguageCode
    text: str
    translations: Optional[List[ConjugationDBMinimal]] = None
    sentences: Optional[List['SentenceDBMinimal']] = None
    article: Optional[str] = None
    case: Optional[Case] = None
    gender: Optional[Gender] = None
    plurality: Optional[Plurality] = None
    politeness: Optional[Politeness] = None
    emphasis: Optional[Emphasis] = None
    tense: Optional[str] = None

    @property
    def unique_fields(self):
        return ['user_id', 'language_code', 'text']


class ConjugationUIMinimal(BaseModel):
    """
    Minimal representation of a conjugation in the UI.
    Does not include individual words or user tracking
    """
    id: str  # UUID
    languageCode: LanguageCode
    text: str
    audioFile: Optional[str] = None  # Relative path from the UI's perspective


class ConjugationUI(BaseModel):
    id: Optional[str] = None  # UUID. Set by the database.
    user: UserUI
    order: int  # Relative to SentenceUI
    tracking: Optional[ProgressTrackerUI]
    language_code: LanguageCode
    text: str
    translations: Optional[List[ConjugationUIMinimal]] = None
    examples: Optional[List['SentenceUIMinimal']] = None
    article: Optional[str] = None
    case: Optional[Case] = None
    gender: Optional[Gender] = None
    plurality: Optional[Plurality] = None
    politeness: Optional[Politeness] = None
    emphasis: Optional[Emphasis] = None
    tense: Optional[str] = None
