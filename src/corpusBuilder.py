import Lyrics
import API_Keys
import csv
import spotipy
from lyricsgenius import Genius, genius
from spotipy.oauth2 import SpotifyClientCredentials
from nltk.tokenize import RegexpTokenizer
from nltk.stem.wordnet import WordNetLemmatizer
from gensim.corpora import Dictionary
from gensim.models import Phrases

import re
import logging
import time
USER = 'spotify'  # all of our playlists will be coming from spotify
# this is the top hits playlist, used for building test corpus
TOP_HITS_ID = '37i9dQZF1DXcBWIGoYBM5M'
PLAYLIST_FILTER = set(['37i9dQZF1DX10zKzsJ2jva', '37i9dQZF1DX4sWSpwq3LiO'])


def getSongInfo(song):
    title = song['track']['name']
    artist = song['track']['artists'][0]['name']
    lyrics = Lyrics.getSongLyrics(title, artist, genius)
    if lyrics == None:
        return(None, None, None)
    return(title, artist, lyrics)


def removeGeniusTags(lyrics):
    # remove genius tags: [verse 1], [chorus], etc
    while re.search('\[.*\]', lyrics):
        lyrics = re.sub('\[.*\]', '', lyrics)
    return(lyrics)


def tokenizeSong(lyrics):
    lyrics = lyrics.lower()
    doc = tokenizer.tokenize(lyrics)
    doc = [token for token in doc if (
        not token.isnumeric()) and len(token) > 1]
    doc = [token for token in doc if token.isascii()]
    doc = [lemmatizer.lemmatize(token) for token in doc]
    return(doc)


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
    genius.sleep_time = 1

    tokenizer = RegexpTokenizer(r'\w+')
    lemmatizer = WordNetLemmatizer()

    playlists = sp.user_playlists(USER)
    playlistsUsed = set()
    docs = []
    with open('songsUsed.csv', mode='w', newline='') as songsUsed:
        songsUsedWriter = csv.writer(
            songsUsed, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        while len(playlistsUsed) <= 2:
            for i, playlist in enumerate(playlists['items']):
                if len(playlistsUsed) > 2:
                    break
                playlistID = playlist['id']
                if playlistID in playlistsUsed.union(PLAYLIST_FILTER):
                    continue
                playlistsUsed.add(playlistID)
                print("geting songs from %d : %s" % (i, playlist['name']))
                songs = Lyrics.get_playlist_tracks(USER, playlistID, sp)
                for song in songs:
                    title, artist, lyrics = getSongInfo(song)
                    if title == None:
                        print("failed to get lyrics for %s, %s" %
                              (title, artist))
                        continue
                    songsUsedWriter.writerow([title, artist])
                    lyrics = removeGeniusTags(lyrics)
                    doc = tokenizeSong(lyrics)
                    _ = ' '.join(doc)  # TODO remove, only here for test
                    docs.append(doc)
            playlists = sp.next(playlists)


# compute bigrams for dictionary
    bigram = Phrases(docs, min_count=20)
    for idx in range(len(docs)):
        for token in bigram[docs[idx]]:
            if '_' in token:
                # Token is a bigram, add to document.
                docs[idx].append(token)

    dictionary = Dictionary(docs)
    dictionary.filter_extremes(no_below=5, no_above=0.75)
    corpus = [dictionary.doc2bow(doc) for doc in docs]

    with open('corpus.txt', mode='w') as corpus:
        for doc in docs:
            corpus.write(" ".join(doc))
            corpus.write("\n")
