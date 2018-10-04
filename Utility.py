import requests
import re
from bs4 import BeautifulSoup
import os
class Utility:

    client_info = {}
    scope = 'playlist-modify-private'
    redirect_uri = 'http://google.com/'
    billboard = "https://www.billboard.com/charts/hot-100"

    def getPlaylistID(self):
        try:
            with open("PlaylistID.txt", "r") as file:
                return file.readline()
        except:
            return None

    def savePlaylistID(self, playlist_id):
        with open("PlaylistID.txt", "w+") as file:
            file.write(playlist_id)

    def playlistExist(self):
        try:
            return os.stat('PlaylistID.txt').st_size==0
        except:
            return False

    def read_file(self):
        try:
            with open("ClientInfo.txt", "r") as file:
                for line in file:
                    try:
                        self.client_info[line.split(":")[0]] = line.split(":")[1].strip()
                    except:
                        return False
                return True
        except IOError:
            self.createClientFile()
            return False
        
    def createClientFile(self):
        with open("ClientInfo.txt", 'w+') as file:
            file.write("Client_ID:\n")
            file.write("Client_Secret:\n")
            file.write("Username:\n")

    def getTrackAndArtist(self):
        page = requests.get(self.billboard)
        soup = BeautifulSoup(page.content, "html.parser")
        songs = soup.find_all('div', class_ ="chart-number-one__title") + soup.find_all('div', class_="chart-list-item__title")
        artists = soup.find_all('div', class_="chart-number-one__artist") + soup.find_all('div', class_="chart-list-item__artist")
        track = [t.get_text(strip = True) for t in songs]
        artist = [re.split(', | & | Featuring ', a.get_text(strip = True)) for a in artists]
        return track, artist
