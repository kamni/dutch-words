import string

from .audio import download_audio
from ..models import (
    Document,
    Sentence,
    SentenceOrder,
    Word,
    WordOrder,
)


def create_sentences_and_words(instance: Document):
    """
    After a document is uploaded, create the sentences and words

    :instance: Document to process
    """

    punctuation_remover = str.maketrans('', '', string.punctuation)

    with instance.doc_file.open('r') as doc_file:
        doc_lines = doc_file.readlines()

    doc = [line.strip() for line in doc_lines]
    for idx, sentence_text in enumerate(doc):
        existing_sentence = Sentence.objects.filter(
            user=instance.user,
            language=instance.language,
            text=sentence_text,
        ).first()
        if existing_sentence:
            sentence = existing_sentence
        else:
            sentence = Sentence.objects.create(
                user=instance.user,
                language=instance.language,
                text=sentence_text,
            )
            audio_file = download_audio(
                user_id=instance.user.id,
                text_id=sentence.id,
                text=sentence.text.translate(punctuation_remover),
                language_code=sentence.language,
            )
            sentence.audio_file.name = audio_file
            sentence.save()

        SentenceOrder.objects.create(
            document=instance,
            sentence=sentence,
            order=idx+1,
        )

        sentence_words = [
            word.translate(punctuation_remover).strip()
            for word in sentence_text.split(' ')
        ]
        for jdx, word_text in enumerate(sentence_words):
            existing_word = Word.objects.filter(
                user=instance.user,
                language=instance.language,
                root_word=word_text,
            ).first()
            if existing_word:
                word = existing_word
            else:
                word = Word.objects.create(
                    user=instance.user,
                    language=instance.language,
                    type=Word.PartOfSpeechType.unknown,
                    root_word=word_text,
                )

            WordOrder.objects.create(
                sentence=sentence,
                word=word,
                order=jdx,
            )
