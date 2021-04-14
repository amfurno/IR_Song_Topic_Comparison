# how to run the app
1. get api keys for the Spotify and Genius API's. I used "https://google.com" as my redirect URIs for simplicity but use whatever you prefer. Place the appropriate keys in the [API keys](src/API_Keys.py)
2. Build your corpus of cleaned documents by running the [corpus builder](src/corpusBuilder.py) file. By default this uses the first 50 playlists published by Spotify in the order they appear on their Playlists page. This file will generate `songsUsed.csv` which contains the title and artists of all songs used, `songLyrics.txt` which has the processes lyrics for every song, and `corpus.txt` which includes bigrams created from the song lyrics. You can adjust the number of playlists used to adjust the corpus size.
3. Build the LDA model using the [modelBuilder](src/modelBuilder.py). THis will build an LDA model based on the corpus, then save it to `LDA_Song_Model`
4. run the GUI app which will load the model from `LDA_Song_Moedl` and then compare songs
