import spacy
from spacy_langdetect import LanguageDetector
from spacy.language import Language
from googletrans import Translator
from collections import Counter
from string import punctuation
import re


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


def get_hotwords(text, tags, nlp):
    result = []
    pos_tag = tags
    doc = nlp(text.lower()) 

    url_pattern = re.compile(r'https?://\S+|www\.\S+')

    for token in doc:
        if token.lemma_ in nlp.Defaults.stop_words or token.text in punctuation:
            continue
        if url_pattern.match(token.text):  
            continue
        if token.pos_ in pos_tag:
            result.append(token.lemma_)
    return list(set(result))


def get_all_hotwords(text):
    language = detect_language(text)
    nlp = spacy.load("./crypto_model")

    if language != 'ru' and language != 'en':
        text = translate_text_to_en(text)

    doc = nlp(text)

    entity_texts = [ent.text for ent in doc.ents]

    return entity_texts
