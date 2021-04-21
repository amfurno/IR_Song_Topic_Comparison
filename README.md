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
- [numpy](https://pypi.org/project/numpy/)
- [pytest](https://pypi.org/project/pytest/)

## API's Used
- [Spotify](https://developer.spotify.com/)
- [Genius Lyrics](https://docs.genius.com/)
