import re
import sys

from nltk.corpus import stopwords

STOP_WORDS = set(stopwords.words('english'))
moreStopWords = set(
    "ah aah aaah aaaah aaaaah ahh ahhhh yee yah huh nah na oh ohh ohhh \
        ohhhh ohhhhh ohhhhhh ohhhhhhh ohhhhhhhh mmm ooh oooh ooooh oooooh doo \
        uh uhh uhhh ayy hmm said gonna".split())


# gets all the songs in a playlist
# method needed b/c user_playlist_tracks only gets 100 songs at a time
def get_playlist_tracks(username, playlist_id, sp):
    results = sp.user_playlist_tracks(username, playlist_id)
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
        def f(obj): return str(obj).encode(
            enc, errors='backslashreplace').decode(enc)
        print(*map(f, objects), sep=sep, end=end, file=file)


def getSongLyrics(title, artistName, genius):
    retries = 0
    songs = None
    url = None
    firstTtileWord = title.split()[0]
    firstTtileWord = formatWord(firstTtileWord)
    title = re.sub('feat\. ', '', title)
    while retries < 3:
        try:
            songs = genius.search_songs(title + ' ' + artistName)
            genius.sleep_time = 2
            break
        except:
            genius.sleep_time *= 2
            retries += 1

    if songs == None or len(songs['hits']) < 1:
        return None
    for hit in songs['hits']:
        hitTitle = hit['result']['title'].split()[0]
        hitTitle = formatWord(hitTitle)
        if firstTtileWord == hitTitle:
            url = hit['result']['url']
            break
    if url == None:
        return None
    song_lyrics = genius.lyrics(song_url=url)
    return(song_lyrics)


def formatWord(word):
    word = word.lower().encode("ascii", "ignore")
    word = word.decode()
    return(word)


def getPlaylists(user, sp):
    playlists = sp.user_playlists(user)
    for _ in range(2):
        for i, playlist in enumerate(playlists['items']):
            uprint("%d %s %s" % (i,  playlist['name'], playlist['id']))
        if playlists['next']:
            playlists = sp.next(playlists)
        else:
            playlists = None


def removeGeniusTags(lyrics):
    # remove genius tags: [verse 1], [chorus], etc
    while re.search('\[.*\]', lyrics):
        lyrics = re.sub('\[.*\]', '', lyrics)
    return(lyrics)


def tokenizeSong(lyrics, tk, lm):
    lyrics = lyrics.lower()
    doc = tk.tokenize(lyrics)
    doc = [token for token in doc if (
        not token.isnumeric()) and len(token) > 2]
    doc = [token for token in doc if (not token in STOP_WORDS
                                      and not token in moreStopWords)]
    doc = [token for token in doc if token.isascii()]
    doc = [lm.lemmatize(token) for token in doc]
    return(doc)
