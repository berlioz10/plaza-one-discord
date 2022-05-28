from asyncio import sleep
import json
import requests
from bs4 import BeautifulSoup
from selenium import webdriver

def get_song_details():
    url = "https://api.plaza.one/status"
    
    response = requests.get(url)
    song = json.loads(response.text)['song']

    return song['artist'], song['title'], song['album'], song['position'], song['length']

get_song_details()

