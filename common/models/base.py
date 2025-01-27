"""
Copyright (C) J Leadbetter <j@jleadbetter.com>
Affero GPL v3
"""

from typing import Any


class HashableDBMixin:
    """
    Implement hashing for DB models.

    A `unique_fields` method must be implemented on the model.

    NOTE: Pydantic has its own hash, but only if the instance is frozen,
    i.e., it can't be updated. This is why we're implementing our own hash.
    """

    def __eq__(self, other: Any) -> bool:
        return hash(self) == hash(other)

    def __hash__(self):
        unique_values = {
            field: self.getattr(field)
            for field in self.unique_fields
        }
        hashstr = f'{self.__class__.__qualname__}-{unique_values}'
        return hash(hashstr)

    @property
    def unique_fields(self):
        """
        List of field names that make a model unique.
        """

        raise NotImplementedError
