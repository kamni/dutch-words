"""
Copyright (C) J Leadbetter <j@jleadbetter.com>
Affero GPL v3
"""

class ObjectExistsError(Exception):
    """
    Thrown when trying to add an object that already exists.
    """
    pass

class ObjectNotFoundError(Exception):
    """
    Thrown when trying to retrieve an object that doesn't exist.
    """
    pass
