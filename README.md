# IR_Song_Topic_Comparison
an app that semantically compares songs to determine if they have similar topics or not

## setup instructions
1. from the `IR_Song_Topic_Comparison` folder activate the virtual environment
  -  Windows : `LDA_Lyric_Comparison\Scripts\activate.bat`
  -  Mac : `source LDA_Lyric_Comparison/bin/activate`
2. get API keys from spotify and Genius
  -  To get these create a developer account on each site and then make an app. This will generate the necessary keys.
3. Run the corpus builder file.
  -  note that the Genius API limits users to 5000 API calls per day by default, so to get all songs you will either need to run this over multiple days, request permistion, or use a smaller corpus
-  This will create an `output` directory with 3 files in it. `songsUsed.csv` contains the title and artists of all songs used, `songLyrics.txt` will contain the processed lyrics from all songs, and `corpus.txt` contains the file corpus with 1 document per row, where each row contains the words and bigrams for the documents.
4. Run the model builder to create and LDA model. 
  -  If this function is run independently, it will generate a model with a number of topics defined by `NUMBER_OF_TOPICS` and store it to `outputs/model/model`. The model contains a number of files that all start with model, and will be loaded into memory for the app. 
  -  The `modelBuilder` method can also be called independently, taking an argument of the number of topics desired, and returning an LDA model build with `corpus.txt`.
5. Run the gui. 
    -  This loads the model into memory and creates a simple gui. Song/artist pairs can be input,and if they can be found in the API's, their topics are compared and a result is given. For more information see the [file descriptions](src/readme.md)

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
This is where keys for the Spotify and Genius API's should be place. You will need to generate your own keys. You can do this by creating apps for both API's (links above) and entering the keys generated.


## Cleaning songs lyrics
"Garbage in, garbage out" is often quoted for building natural language model, and so the lyrics go through a fair bit of processing.
- Genius tags are removed. These denote sections of the songs: [chorus], [verse 1], etc and have no semantic meaning
- lowercase and tokenize. Every word is converted to lowercase, words that contain numbers are removed, and words are split on any punctuation
- lemmatize. This combines words that have the same semantic meaning. This is done by the [NLTK lemmatizer](http://www.nltk.org/api/nltk.stem.html#nltk.stem.wordnet.WordNetLemmatizer)
- remove stop words. The stop words are a combination of [NLTK Enlish Stop words](https://www.nltk.org/book/ch02.html) and stop words unique to song lyrics ("ahhh", "oooh", "huh", etc).
