import spacy
from spacy_langdetect import LanguageDetector
from spacy.language import Language
from googletrans import Translator
from collections import Counter
from string import punctuation
import re

MY_STOPWORDS = {'http', 'https', 'gmgn', 'gm', 'gn', 'airdrop', 'early', 'wallet', 'claim', 'discord', 'user',
                 'email', 'season', 'code', 'task', 'submit', 'nft', 'com', 'app', 'token', 'google', 'remind',
                 'notice', 'status', 'article', 'xyz', 'feed', 'edition', 'www', 'gle', 'forms', 'twitter', 
                 'emoji', 'otc', 'ceo', 'web3'}

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


def get_hotwords(text, tags, nlp, custom_stop_words):
    result = []
    pos_tag = tags
    doc = nlp(text.lower()) 

    if custom_stop_words:
        for word in custom_stop_words:
            nlp.Defaults.stop_words.add(word)
            nlp.vocab[word].is_stop = True

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

    # flag = True
    if language == 'ru':
        nlp = spacy.load("ru_core_news_sm")
        # flag = False
    elif language == 'en':
        nlp = spacy.load("en_core_web_sm")
    else:
        text = translate_text_to_en(text)
        nlp = spacy.load("en_core_web_sm")
        # flag = False

    propn = set(get_hotwords(text, 'PROPN', nlp, MY_STOPWORDS))
    most_common_propn = Counter(propn).most_common(5)
    most_common_propn = [word for word, _ in most_common_propn]

    return most_common_propn

    # if not flag:
    #     return most_common_propn
    
    # other = set(get_hotwords(text, ['NOUN'], nlp))
    # most_common_other = Counter(other).most_common(5)
    # most_common_other = [word for word, _ in most_common_other]
  
    # return most_common_propn + most_common_other
