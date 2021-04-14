# IR_Song_Topic_Comparison
an app that semantically compares songs to determine if they have similar topics or not

## setup instructions
1. from the `IR_Song_Topic_Comparison` folder activated the virtual environment
-  Windows : `LDA_Lyric_Comparison\Scripts\activate.bat`
-  Mac : `source LDA_Lyric_Comparison/bin/activate`
2. get API keys from spotify and Genius
3. run the app

## packages used:
- [gensim](https://pypi.org/project/gensim/)
- [spotipy](https://pypi.org/project/spotipy/)
- [nltk](https://pypi.org/project/nltk/)
- [lyricsgenius](https://pypi.org/project/lyricsgenius/)
- [autopep8](https://pypi.org/project/autopep8/)
- [numpy](https://pypi.org/project/numpy/)
- [pytest](https://pypi.org/project/pytest/)

## API's Used
- [Spotify](https://developer.spotify.com/)
- [Genius Lyrics](https://docs.genius.com/)

## File Descriptions

### Lyrics.py
This file contains a number of functions that get information from either the Spotify API or the Genius API. 

### corpusBuilder.py
This file builds the corpus that will be used to create the LDA model. It uses the firt 100 playlists published by Spotify. The order of playlists is the same order as they appear on Spotify's playlist page. Two playlist are excluded: "Peaceful Piano", because it is all instrumental, and "Viva Latino", because the Spanish words are not compadible with an LDA model build using English words. The lyrics to each song are cleaned and tokenized, then written to `corpus.txt`, where each line is a new song. A list of songs and their artists is stored in `songsUsed.csv`

### API_Keys.py
This is where keys for the Spotify and Genius API's should be place. You will need to generate your own keys. You can do this by creating and apps for both API's (links above) and entering the keys generated.


## Cleaning songs lyrics
"Garbage in, garbage out" is often quoted for building natural language model, and so the lyrics go through a fair bit of processing.
- Genius tags are removed. These denote sections of the songs: [chorus], [verse 1], etc and have no semantic meaning
- lowercase and tokenize. Every word is converted to lowercase, words that contain numbers are removed, and words are split on any punctuation
- lemmatize. This combines words that have the same semantic meaning. This is done by the [NLTK lemmatizer](http://www.nltk.org/api/nltk.stem.html#nltk.stem.wordnet.WordNetLemmatizer)
- remove stop words. The stop words are a combination of [NLTK Enlish Stop words](https://www.nltk.org/book/ch02.html) and stop words unique to song lyrics ("ahhh", "oooh", "huh", etc).
