import os
import json
import spotipy
from lyricsgenius import Genius, genius
from spotipy.oauth2 import SpotifyClientCredentials
import API_Keys

auth_manager = SpotifyClientCredentials(client_id=API_Keys.spotify_client_id, client_secret=API_Keys.spotify_secret)
sp = spotipy.Spotify(auth_manager=auth_manager)

# gets all the songs in a playlist
# method needed b/c user_playlist_tracks only gets 100 songs at a time
def get_playlist_tracks(username,playlist_id):
    results = sp.user_playlist_tracks(username,playlist_id)
    tracks = results['items']
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    return tracks


#gets all of a user's public playlists
playlists = sp.user_playlists('paiqwghgo8plz5ystl4t9plar')
# while playlists:
#     for i, playlist in enumerate(playlists['items']):
#         print("%4d %s %s" % (i + 1 + playlists['offset'], playlist['uri'],  playlist['name']))
#     if playlists['next']:
#         playlists = sp.next(playlists)
#     else:
#         playlists = None

tracks = get_playlist_tracks("paiqwghgo8plz5ystl4t9plar", playlists['items'][0]['id'])

songTitle = tracks[0]['track']['name']
songArtist = tracks[0]['track']['artists'][0]['name']

genius = Genius(API_Keys.genius_access_token)
artist = genius.search_artist(songArtist, max_songs=3, sort = 'title')
song = artist.song(songTitle)
print(song.lyrics)
