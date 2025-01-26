"""
Copyright (C) J Leadbetter <j@jleadbetter.com>
Affero GPL v3

NOTE: A 'conjugation' in this context is a variation on a root word.
For example, the English verb 'to go' has multiple conjugations.
such as 'went', 'goes', 'will have gone'.
"""

from enum import Enum
from typing import Optional

from pydantic import BaseModel

from .tracking import ProgressTrackerUI
from .words import WordDBMinimal, WordUI
from .users import UserUI
from ..utils.languages import LanguageCode


class Case(str, Enum):
    nominative = 'nominative'
    accusative = 'accusative'
    dative = 'dative'
    genitive = 'genitive'


class Person(str, Enum):
    first = 'first'
    second = 'second'
    third = 'third'


class Plurality(str, Enum):
    single = 'single'
    plural = 'plural'


class Gender(str, Enum):
    neutral = 'neutral'
    feminine = 'feminine'
    masculine = 'masculine'


class Politeness(str, Enum):
    casual = 'casual'
    formal = 'formal'


class Emphasis(str, Enum):
    stressed = 'stressed'
    unstressed = 'unstressed'


class ConjugationDBMinimal(BaseModel):
    """
    Minimal representation of a conjugation stored in the database
    """

    id: str  # UUID
    sentence_id: str  # UUID
    tracking_id: str  # UUID
    order: int  # Relative to the SentenceDB


class ConjugationDB(BaseModel):
    """
    Representation of a conjugation in the Database.
    """

    id: Optional[str] = None  # UUID. Set by the database.
    user_id: str  # UUID.
    tracking_id: Optional[str]  # UUID
    order: int  # Relative to SentenceDB
    word: WordDBMinimal
    language_code: LanguageCode
    text: str
    translations: Optional[List[ConjugationDBMinimal]] = None
    examples: Optional[List['SentenceDBMinimal']] = None
    article: Optional[str] = None
    case: Optional[Case] = None
    gender: Optional[Gender] = None
    plurality: Optional[Plurality] = None
    politeness: Optional[Politeness] = None
    emphasis: Optional[Emphasis] = None
    tense: Optional[str] = None


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
    word: WordUI
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
