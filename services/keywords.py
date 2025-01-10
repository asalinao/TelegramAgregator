import spacy
from spacy_langdetect import LanguageDetector
from spacy.language import Language
from googletrans import Translator

def detect_language(text):
    nlp = spacy.load("en_core_web_sm")
    @Language.factory("language_detector")
    def create_language_detector(nlp, name):
        return LanguageDetector()

    nlp.add_pipe("language_detector", last=True)

    doc = nlp(text)

    if doc._.language['score'] > 0.75:
        return doc._.language['language']
    else:
        'unknown'


def translate_text_to_en(text):
    translator = Translator()
    translated_text = translator.translate(str(text), dest='en').text
    return translated_text


def get_all_hotwords(text):
    language = detect_language(text)
    nlp = spacy.load("./crypto_model")

    if language != 'ru' and language != 'en':
        text = translate_text_to_en(text)

    doc = nlp(text)


    tickers = [ent.text for ent in doc.ents if ent.label_ == 'TOKEN_NAME']
    keywords = [ent.text for ent in doc.ents if ent.label_ != 'TOKEN_NAME']

    i = 0
    while i < len(tickers):
        if tickers[i][0] != '$':
            keywords.append(tickers.pop(i))
        else:
            tickers[i] = tickers[i].upper()
            i += 1

    annotations = []
    for ent in doc.ents:
        annotations.append({
            "value": {
                "start": ent.start_char,
                "end": ent.end_char,
                "text": ent.text,
                "labels": [ent.label_]
            },
            "id": f"annotation_{ent.start_char}_{ent.end_char}",
            "from_name": "label",
            "to_name": "text",
            "type": "labels",
            "origin": "model"
        })

    result_json = {
        "annotations": [
            {
                "result": annotations,
            }
        ],
        "data": {
            "text": text
        }
    }

    return tickers, keywords, result_json

