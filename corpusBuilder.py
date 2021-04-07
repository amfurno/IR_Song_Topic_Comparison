import Lyrics
import API_Keys
import spotipy
from lyricsgenius import Genius, genius
from spotipy.oauth2 import SpotifyClientCredentials
from nltk.tokenize import RegexpTokenizer

USER = 'spotify' #all of our playlists will be coming from spotify
TOP_HITS_ID = '37i9dQZF1DXcBWIGoYBM5M' #this is the top hits playlist, used for building test corpus

if __name__ == '__main__':
    corpus = open("corpus.txt", "r")

    auth_manager = SpotifyClientCredentials(client_id=API_Keys.spotify_client_id, client_secret=API_Keys.spotify_secret)
    sp = spotipy.Spotify(auth_manager=auth_manager)

    genius = Genius(API_Keys.genius_access_token)

    tokenizer = RegexpTokenizer(r'\w+')
    
    playist = sp.user_playlist(USER, TOP_HITS_ID)
    songs = Lyrics.get_playlist_tracks(USER, TOP_HITS_ID, sp)
    for song in songs:
        title = song['track']['name']
        artist = song['track']['artists'][0]['name']
        doc = Lyrics.getSongLyrics(title, artist, genius)
        doc = doc.lower()
        doc = tokenizer.tokenize(doc)
        print(doc)
        #corpus.write(str(doc))
        
        


