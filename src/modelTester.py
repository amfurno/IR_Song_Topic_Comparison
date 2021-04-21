import csv
from itertools import combinations

from lyricsgenius import Genius
from API_Keys import genius_access_token
import modelBuilder as builder
import songComparison as compare


NUMBER_OF_TOPICS = [5, 6, 7, 8, 9, 10, 11, 12, 13,
                    14, 15, 20, 25, 30, 40, 50, 75, 100, 200, 300, 400]


def runTest(model, songPair, songLyrics):
    song1, song2 = songPair[0], songPair[1]
    song1Title = song1[0]
    song2Title = song2[0]
    song1Lyrics = songLyrics[song1Title]
    song2Lyrics = songLyrics[song2Title]
    docs = [song1Lyrics, song2Lyrics]
    dist = compare.getSongDivergence(model, docs)

    if dist <= .2 and song1[2] == song2[2]:
        return 1
    if dist > .2 and song1[2] != song2[2]:
        return 1
    else:
        return 0


if __name__ == '__main__':
    trainedSongs = []
    untrainedSongs = []
    songLyrics = {}

    genius = Genius(genius_access_token)
    genius.timeout = 15
    genius.sleep_time = 2

    with open("testSongList.csv", mode='r', newline='') as songs:
        songReader = csv.reader(songs, delimiter=',', quotechar='"')
        next(songReader, None)
        for song in songReader:
            doc = compare.getLyrics(song[0], song[1], genius)
            songLyrics[song[0]] = doc
            if song[3] == 'y':
                trainedSongs.append(song)
            else:
                untrainedSongs.append(song)

    with open("outputs/testResults.csv", mode='a', newline='') as results:
        resultsWriter = csv.writer(results, delimiter=',', quotechar='"')
        resultsWriter.writerow(
            ['number of topics',
                '% trained song comparisons correct',
                '% untrained song comparisons correct',
                '% song comparisons correct for all songs',
             ])

        for num_Topic in NUMBER_OF_TOPICS:
            model = builder.modelBuilder(num_Topic)
            results = []
            results.append(num_Topic)

            trainedResults = []
            for pair in combinations(trainedSongs, 2):
                result = runTest(model, pair, songLyrics)
                trainedResults.append(result)
            score = sum(trainedResults)/len(trainedResults)
            results.append(score)
            print("trained finished")

            untrainedResults = []
            for pair in combinations(untrainedSongs, 2):
                result = runTest(model, pair, songLyrics)
                untrainedResults.append(result)
            score = sum(untrainedResults)/len(untrainedResults)
            results.append(score)
            print("untrained finished")

            allSongResults = []
            allSongs = trainedSongs + untrainedSongs
            for pair in combinations(allSongs, 2):
                result = runTest(model, pair, songLyrics)
                allSongResults.append(result)
            score = sum(allSongResults)/len(allSongResults)
            results.append(score)

            resultsWriter.writerow(results)
