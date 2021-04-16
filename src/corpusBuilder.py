import Lyrics
import API_Keys
import csv
import spotipy
from gensim.models import Phrases
from lyricsgenius import Genius, genius
from nltk.tokenize import RegexpTokenizer
from nltk.stem.wordnet import WordNetLemmatizer
from spotipy.oauth2 import SpotifyClientCredentials

import re
import logging
USER = 'spotify'  # all of our playlists will be coming from spotify
# this is the top hits playlist, used for building test corpus
TOP_HITS_ID = '37i9dQZF1DXcBWIGoYBM5M'
PLAYLIST_FILTER = set(['37i9dQZF1DX10zKzsJ2jva', '37i9dQZF1DX4sWSpwq3LiO'])


def getSongInfo(song):
    if song['track'] is not None and song['track']['name'] is not None:
        title = song['track']['name']
    else:
        return(None, None, None)
    if (song['track']['artists'] is not None and
            song['track']['artists'][0] is not None and
            song['track']['artists'][0]['name'] is not None):
        artist = song['track']['artists'][0]['name']
    else:
        return(None, None, None)
    lyrics = Lyrics.getSongLyrics(title, artist, genius)
    return(title, artist, lyrics)


if __name__ == '__main__':
    logging.basicConfig(
        format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

    # api authentication tokens
    auth_manager = SpotifyClientCredentials(
        client_id=API_Keys.spotify_client_id, client_secret=API_Keys.spotify_secret)
    sp = spotipy.Spotify(auth_manager=auth_manager)
    genius = Genius(API_Keys.genius_access_token)
    genius.excluded_terms = ["(Remix)", "(Live)"]
    genius.timeout = 15
    genius.sleep_time = 2

    tokenizer = RegexpTokenizer(r'\w+')
    lemmatizer = WordNetLemmatizer()

    playlists = sp.user_playlists(USER)
    playlistsUsed = set()
    docs = []
    songsUsed = set()

    with open('outputs/songsUsed.csv', mode='w', newline='') as songsUsedCSV, open('outputs/songLyrics.txt', mode='w') as songLyrics:
        songsUsedWriter = csv.writer(
            songsUsedCSV, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        while len(playlistsUsed) <= 50:
            for i, playlist in enumerate(playlists['items']):
                if len(playlistsUsed) > 49:
                    break
                playlistID = playlist['id']
                if playlistID in playlistsUsed.union(PLAYLIST_FILTER):
                    continue
                playlistsUsed.add(playlistID)
                print("geting songs from %d : %s" % (i, playlist['name']))
                songs = Lyrics.get_playlist_tracks(USER, playlistID, sp)
                for song in songs:
                    if song['track'] is None:
                        continue
                    if song['track']['id'] in songsUsed:
                        continue
                    else:
                        songsUsed.add(song['track']['id'])

                    title, artist, lyrics = getSongInfo(song)
                    if lyrics == None:
                        print("failed to get lyrics for %s, %s" %
                              (title, artist))
                        continue

                    songsUsedWriter.writerow([title, artist])
                    lyrics = Lyrics.removeGeniusTags(lyrics)
                    doc = Lyrics.tokenizeSong(lyrics, tokenizer, lemmatizer)
                    songLyrics.write(' '.join(doc) + '\n')
                    docs.append(doc)
            playlists = sp.next(playlists)


# compute bigrams for dictionary
    bigram = Phrases(docs, min_count=20)
    for idx in range(len(docs)):
        for token in bigram[docs[idx]]:
            if '_' in token:
                # Token is a bigram, add to document.
                docs[idx].append(token)

    with open('outputs/corpus.txt', mode='w') as corpus:
        for doc in docs:
            corpus.write(" ".join(doc))
            corpus.write("\n")
