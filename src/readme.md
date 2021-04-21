## File Descriptions

### Lyrics.py
This file contains a number of functions that get information from either the Spotify API or the Genius API. 

### corpusBuilder.py
This file builds the corpus that will be used to create the LDA model. It uses the first 100 playlists published by Spotify. The order of playlists is the same order as they appear on Spotify's playlist page. Two playlist are excluded: "Peaceful Piano", because it is all instrumental, and "Viva Latino", because the Spanish words are not compadible with an LDA model build using English words. The lyrics to each song are cleaned and tokenized, then written to `corpus.txt`, where each line is a new song. A list of songs and their artists is stored in `songsUsed.csv`

### API_Keys.py
This is where keys for the Spotify and Genius API's should be placed. You will need to generate your own keys. You can do this by creating apps for both API's (links above) and entering the keys generated.

### modelBuilder.py
This is the file that actually builds the LDA model. It can be run independently, which builds a model and stores it in outputs/model/model, or the `buildModel` function can be called directly from somewhere else. This allows the model creation to take place independently without inadvertantly overwriting the model that is currenlty saved. This is where all parameter tuning can be done. Number of topics sit the parameter most likely to change, and thus is set by a function argument, but all other parameters can be changed here as well.

### modelTester.py
This file is what we used to test the models. It builds a model and then uses the songs selected in `testSongList.csv` to compare to each other. Each model is scored based on how many true positives and true negatives it identifies. The scores are then writtne to a csv file. 

### gui.py
This file generates a gui for the end user to interact with. It relies on having a model already build and stored that it can load and utilize. This allows quick startup so it does not have to build a new model every time it is run. However, this necessitates that a model already be build when the gui is ran. Song information is entered and is used to query the Spotify and Genius API's. The lyrics are then clean exactly how the original corpus was and compared to the model. Comparing to the model generates a spare array of the form [[int, float]] for each topic, probability pair with a probability greater than 0. These are then converted to full arrays and compared using Jensen-Shannon Divergence. 

## Cleaning songs lyrics
"Garbage in, garbage out" is often quoted for building natural language model, and so the lyrics go through a fair bit of processing.
- Genius tags are removed. These denote sections of the songs: [chorus], [verse 1], etc and have no semantic meaning
- lowercase and tokenize. Every word is converted to lowercase, words that contain numbers are removed, and words are split on any punctuation
- lemmatize. This combines words that have the same semantic meaning. This is done by the [NLTK lemmatizer](http://www.nltk.org/api/nltk.stem.html#nltk.stem.wordnet.WordNetLemmatizer)
- remove stop words. The stop words are a combination of [NLTK Enlish Stop words](https://www.nltk.org/book/ch02.html) and stop words unique to song lyrics ("ahhh", "oooh", "huh", etc).
