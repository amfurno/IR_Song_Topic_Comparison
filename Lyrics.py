import spotipy
from lyricsgenius import Genius, genius
from spotipy.oauth2 import SpotifyClientCredentials
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

def getSongLyrics(title, artistName, genius):
    # artist = geniusToken.search_artist(artistName, max_songs=0, sort = 'title')
    # song = artist.song(title)
    # return(song.lyrics)
    songs = genius.search_songs(title + ' ' + artistName)
    url = songs['hits'][0]['result']['url']
    song_lyrics = genius.lyrics(song_url=url)
    return(song_lyrics)



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

