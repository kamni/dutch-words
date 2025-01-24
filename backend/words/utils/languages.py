import os
from typing import List, Tuple

from django.utils.translation import gettext_lazy as _
from langcodes.registry_parser import parse_registry


def language_choices() -> List[Tuple[str, str]]:
    """
    Get a list of language choices for use in a Django model field.

    :return: List of tuples, e.g. [('en', 'English')]
    """

    choices = [
        (data['Subtag'], _(data['Description'][0]))
        for data in parse_registry()
        if data['Type'] == 'language'
    ]
    return choices
