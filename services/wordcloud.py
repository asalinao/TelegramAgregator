import sqlite3
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from stop_words import get_stop_words
from database.db import get_user_subscribed_channels

def cloud_generate(user_id, filename):
    channels = get_user_subscribed_channels(user_id)
    channels_ids = list(channels.keys())

    conn = sqlite3.connect('subscriptions.db')
    cursor = conn.cursor()

    placeholders = ', '.join(['?'] * len(channels_ids))
    
    cursor.execute(f"""
                   SELECT text 
                   FROM Messages 
                   WHERE channel_id IN ({placeholders})
                   AND created_at >= DATETIME('now', '-24 hours')
                   """, channels_ids)
    
    keywords_list = [row[0] for row in cursor.fetchall()]

    keywords = " ".join(keywords_list)

    STOPWORDS_RU = get_stop_words('russian')

    wordcloud = WordCloud(width = 2000, 
                        height = 1500, 
                        random_state=1, 
                        background_color='black', 
                        margin=20, 
                        colormap='Pastel1', 
                        collocations=False, 
                        stopwords = STOPWORDS_RU).generate(keywords)
    
    plt.figure(figsize=(40, 30))
    plt.axis("off") 
    plt.imshow(wordcloud) 
    plt.savefig(filename, bbox_inches='tight') 

