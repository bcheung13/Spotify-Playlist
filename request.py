import requests
import re
from bs4 import BeautifulSoup
import spotipy
import spotipy as util

def tracksAndartists():
    page = requests.get("https://www.billboard.com/charts/hot-100")
    soup = BeautifulSoup(page.content, "html.parser")
    songs = soup.find_all('div', class_ ="chart-number-one__title") + soup.find_all('div', class_="chart-list-item__title")
    artists = soup.find_all('div', class_="chart-number-one__artist") + soup.find_all('div', class_="chart-list-item__artist")


    track = [t.get_text(strip = True) for t in songs]
    artist = [re.split(', | & | Featuring ', a.get_text(strip = True)) for a in artists]
    return track, artist


