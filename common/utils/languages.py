from enum import Enum

from langcodes.registry_parser import parse_registry


# ISO 639 language codes
LanguageCode = Enum(
    'LanguageCode',
    {
        data['Subtag']: data['Subtag'].lower()
        for data in parse_registry()
        if data['Type'] == 'language'
    },
)
