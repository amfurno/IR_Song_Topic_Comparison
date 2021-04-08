import Lyrics
import API_Keys
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
USER = 'spotify' #all of our playlists will be coming from spotify
TOP_HITS_ID = '37i9dQZF1DXcBWIGoYBM5M' #this is the top hits playlist, used for building test corpus



if __name__ == '__main__':
    start = time.perf_counter()
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

    docs = []

    auth_manager = SpotifyClientCredentials(client_id=API_Keys.spotify_client_id, client_secret=API_Keys.spotify_secret)
    sp = spotipy.Spotify(auth_manager=auth_manager)

    genius = Genius(API_Keys.genius_access_token)
    genius.excluded_terms = ["(Remix)", "(Live)"]

    tokenizer = RegexpTokenizer(r'\w+')
    lemmatizer = WordNetLemmatizer()
    
    playist = sp.user_playlist(USER, TOP_HITS_ID)
    songs = Lyrics.get_playlist_tracks(USER, TOP_HITS_ID, sp)
    for song in songs:
        title = song['track']['name']
        artist = song['track']['artists'][0]['name']
        Lyrics.uprint("current song:", title)
        lyrics = Lyrics.getSongLyrics(title, artist, genius)

        #remove genius tags: [verse 1], [chorus], etc
        while re.search('\[.*\]', lyrics):
            lyrics = re.sub('\[.*\]', '', lyrics)

        #convert the string to a list of tokens
        lyrics = lyrics.lower()
        doc = tokenizer.tokenize(lyrics)
        doc = [token for token in doc if not token.isnumeric() and len(token) > 1 and token.isalpha()]   
        doc = [lemmatizer.lemmatize(token) for token in doc] 
        docs.append(doc)

        bigram = Phrases(docs, min_count=20)

    finDocs = time.perf_counter()
    print(f"\nfinished gettings song lyrics in {finDocs - start:0.4f} secs\n")  

#compute bigrams for dictionary
    bigram = Phrases(docs, min_count=20)
    for idx in range(len(docs)):
        for token in bigram[docs[idx]]:
            if '_' in token:
                # Token is a bigram, add to document.
                docs[idx].append(token)
    
    finBigrams = time.perf_counter()
    print(f"\nfinished making bigrams in  in {finBigrams - finDocs:0.4f} secs\n")  
    
    dictionary = Dictionary(docs)
    dictionary.filter_extremes(no_below=5, no_above=0.75)
    corpus = [dictionary.doc2bow(doc) for doc in docs]


