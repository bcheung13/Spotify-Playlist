import spotipy
import spotipy.util as util
from datetime import datetime

from Utility import Utility
class Driver:

    def __init__(self):
        u = Utility()  
        if u.read_file():
            token = util.prompt_for_user_token(u.client_info['Username'], u.scope, u.client_info['Client_ID'], u.client_info["Client_Secret"], u.redirect_uri)
            sp = spotipy.Spotify(auth = token)
        else:
            print("Fill out client info.")
            return
        track, artist = u.getTrackAndArtist()
        playlist_id = u.getPlaylistID()
        if playlist_id:
            sp.user_playlist_change_details(u.client_info["Username"], playlist_id, name = f'{datetime.now().month}-{datetime.now().day}-{datetime.now().year}')
        else:
            playlist_id = sp.user_playlist_create(u.client_info['Username'],f'{datetime.now().month}-{datetime.now().day}-{datetime.now().year}',False)['id']
            u.savePlaylistID(playlist_id)
        
        track_id = []
        for t,a in zip(track, artist):
            try:
                track_id.append(sp.search(q=f'artist:{a[0]} track:{t}', type='track')['tracks']['items'][0]['uri'])
            except:
                print(f"Can't find {t} by {a}")
        sp.user_playlist_replace_tracks(u.client_info["Username"], playlist_id, track_id)

Driver()

        