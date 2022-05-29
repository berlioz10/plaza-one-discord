from asyncio import sleep
import json
import requests

def get_song_status():
    url = 'https://api.plaza.one/status'
    
    response = requests.get(url)
    song = json.loads(response.text)['song']

    return song['artist'], song['title'], song['album'], song['position'], song['length'], song['artwork_src']

def get_news():
    url = 'https://api.plaza.one/news'
    
    response = requests.get(url)
    news = json.loads(response.text)
    articles = news['articles'][:3]

    return articles