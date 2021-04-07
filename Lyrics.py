import os
import json
import spotipy
from lyricsgenius import Genius, genius
from spotipy.oauth2 import SpotifyClientCredentials
import API_Keys
import sys


# gets all the songs in a playlist
# method needed b/c user_playlist_tracks only gets 100 songs at a time
def get_playlist_tracks(username,playlist_id, sp):
    results = sp.user_playlist_tracks(username,playlist_id)
    tracks = results['items']
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    return tracks

def uprint(*objects, sep=' ', end='\n', file=sys.stdout):
    enc = file.encoding
    if enc == 'UTF-8':
        print(*objects, sep=sep, end=end, file=file)
    else:
        f = lambda obj: str(obj).encode(enc, errors='backslashreplace').decode(enc)
        print(*map(f, objects), sep=sep, end=end, file=file)

def getPlaylistFollowerCount(user, playlist_id, sp):
    playlist = sp.user_playlist(user, playlist_id)
    return playlist['followers']['total']

def getSongLyrics(title, artistName, geniusToken):
    artist = geniusToken.search_artist(artistName, max_songs=3, sort = 'title')
    song = artist.song(title)
    return(song.lyrics)



#gets all of a user's public playlists
# playlists = sp.user_playlists('spotify')
# while playlists:
#     for i, playlist in enumerate(playlists['items']):
#         uprint("%s %s" % (playlist['uri'],  playlist['name']))
#         # print("followers:", getPlaylistFollowerCount('spotify', playlist['id']))
#         print(playlist['followers']['total'])
#     if playlists['next']:
#         playlists = sp.next(playlists)
#         playlist = None
#     else:
#         playlists = None



# pl = playlists['items'][0]
# print(pl['followers']['total'])
# tracks = get_playlist_tracks("paiqwghgo8plz5ystl4t9plar", playlists['items'][0]['id'])

# songTitle = tracks[0]['track'].keys()
# print(songTitle)
# songArtist = tracks[0]['track']['artists'][0]['name']

# genius = Genius(API_Keys.genius_access_token)
# artist = genius.search_artist(songArtist, max_songs=3, sort = 'title')
# song = artist.song(songTitle)
# print(song.lyrics)
