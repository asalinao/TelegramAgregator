import sqlite3
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from stop_words import get_stop_words

MY_STOPWORDS = ['http', 'https', 'gmgn', 'gm', 'gn', 'airdrop', 'early', 'wallet', 'claim', 'discord', 'user',
                 'email', 'season', 'code', 'task', 'submit', 'nft', 'com', 'app', 'token', 'google', 'remind',
                 'notice', 'status', 'article', 'xyz', 'feed', 'edition', 'www', 'gle']

def cloud_generate(keywords, filename):
    STOPWORDS_RU = get_stop_words('russian')
    STOPWORDS_EN = get_stop_words('en')
    STOPWORDS = STOPWORDS_RU + STOPWORDS_EN + MY_STOPWORDS

    wordcloud = WordCloud(width = 2000, 
                        height = 1500, 
                        random_state=1, 
                        background_color='black', 
                        margin=20, 
                        max_words = 20,
                        colormap='winter', 
                        collocations=False,
                        min_word_length = 3,
                        stopwords = STOPWORDS).generate(keywords)
    
    plt.figure(figsize=(40, 30))
    plt.axis("off") 
    plt.imshow(wordcloud) 
    plt.savefig(filename, bbox_inches='tight',  pad_inches=0) 

