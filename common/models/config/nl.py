"""
Copyright (C) J Leadbetter <j@jleadbetter.com>
Affero GPL v3

Configuration for the Dutch (nl) language.
"""

from copy import deepcopy

from pydantic import BaseModel


def get_config():
    from common.models.words import DEFAULT_CONFIG
    config = deepcopy(DEFAULT_CONFIG)
    del config['NounData']['case']
    del config['AdjectiveData']['case']
    del config['VerbData']['gender']
    del config['VerbData']['politeness']
    return config
