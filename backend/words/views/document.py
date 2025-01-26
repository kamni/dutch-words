"""
Copyright (C) J Leadbetter <j@jleadbetter.com>
Affero GPL v3
"""

from django.conf import settings
from django.http.response import JsonResponse


def document_list(request):
    """
    Return minimal data for listing databases
    """
    document_adapters = None # TODO: create this
    return JsonResponse({})
