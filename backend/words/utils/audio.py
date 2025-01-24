import os
import pathlib

from gtts import gTTS


def get_audio_upload_folder(user_id: int, language_code: str) -> str:
    """
    Helper function for finding the upload folder for audio files.

    You probably want to use the other function, get_tmp_upload_path.

    user_id: Django User id
    language_code: official language code (e.g., 'en' for English)

    :return: path (as string) to folder where audio will be uploaded.
    """

    return os.path.join('uploads', str(user_id), language_code, 'audio')


def get_audio_upload_path(user_id: int, text_id: str, language_code: str) -> str:
    """
    Get the location of uploaded audio files.

    This should primarily be used after either a Word or a Sentence is saved,
    to clean up the tmp file.

    :user_id: Django User id
    :text_id: Either Word.id or Sentence.id.
        If the object hasn't been created yet, just supply a random UUID.
    :language_code: official language code (e.g. 'en' for English)

    :return: path (as string) to audio file
    """

    return os.path.join(
        get_audio_upload_folder(user_id, language_code),
        f'{text_id}.mp3',
    )


def download_audio(user_id: int, text_id: str, text: str, language_code: str) -> str:
    """
    Download audio from the Google TTS API

    :user_id: Django User id
    :text_id: Either Word.id or Sentence.id.
        If the object hasn't been created yet, just supply a random UUID.
    :text: Text to convert to TTS
    :language_code: official language code (e.g., 'en' for English)

    :return: path (as string) where the file was uploaded.
    """

    folder = get_audio_upload_folder(user_id, language_code)
    pathlib.Path(folder).mkdir(parents=True, exist_ok=True)

    file_destination = get_audio_upload_path(user_id, text_id, language_code)
    tts = gTTS(text, lang=language_code)
    tts.save(file_destination)
    return file_destination
