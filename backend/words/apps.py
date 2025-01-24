from django.apps import AppConfig
from django.db.models.signals import post_save


class WordsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'words'

    def ready(self):
        from . import signals
