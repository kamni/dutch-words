from django.contrib import admin

from .models import (
    Conjugation,
    Document,
    Sentence,
    SentenceOrder,
    Word,
    WordOrder,
)


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['display_name', 'language', 'user']


@admin.register(Sentence)
class SentenceAdmin(admin.ModelAdmin):
    list_display = ['text', 'language', 'user']


@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    list_display = ['root_word', 'language', 'user']


@admin.register(WordOrder)
class WordOrderAdmin(admin.ModelAdmin):
    list_display = ['sentence', 'word', 'order']


@admin.register(SentenceOrder)
class SentenceOrderAdmin(admin.ModelAdmin):
    list_display = ['document', 'sentence', 'order']


@admin.register(Conjugation)
class ConjugationAdmin(admin.ModelAdmin):
    list_display = ['text', 'word', 'language', 'user']
