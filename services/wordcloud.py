import gc
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from stop_words import get_stop_words


def cloud_generate(keywords, filename):
    STOPWORDS_RU = get_stop_words('russian')
    STOPWORDS_EN = get_stop_words('en')
    STOPWORDS = STOPWORDS_RU + STOPWORDS_EN

    keywords = keywords.lower()
    keywords = keywords.replace('bitcoin', 'btc')
    keywords = keywords.replace('solana', 'sol')
    keywords = keywords.replace('ethereum', 'eth')

    wordcloud = WordCloud(width = 2000, 
                        height = 1500, 
                        random_state=1, 
                        background_color='black', 
                        margin=20, 
                        max_words = 30,
                        colormap='winter', 
                        collocations=True,
                        min_word_length = 3,
                        stopwords = STOPWORDS).generate(keywords)
    
    plt.figure(figsize=(40, 30))
    plt.axis("off") 
    plt.imshow(wordcloud) 
    plt.savefig(filename, bbox_inches='tight',  pad_inches=0) 

    del wordcloud
    gc.collect

