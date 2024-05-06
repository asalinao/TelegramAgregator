from googletrans import Translator


def translate_text(text):
    translator = Translator()
    translated_text = translator.translate(str(text), dest='ru').text
    return translated_text
