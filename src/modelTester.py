import csv
from itertools import combinations

import modelBuilder as builder
import songComparison as compare

NUMBER_OF_TOPICS = [5]  # , 6, 7, 8, 9, 10, 11, 12, 13, 14, 50, 100


def runTest(model, songPair):
    song1, song2 = songPair[0], songPair[1]
    song1Title = song1[0]
    artist1 = song1[1]
    song2Title = song2[0]
    artist2 = song2[1]
    dist = compare.songComparison(
        model, song1Title, artist1, song2Title, artist2)
    if dist >= .6:
        return 1
    else:
        return 0


if __name__ == '__main__':
    trainedSongs = []
    untrainedSongs = []
    for num_Topic in NUMBER_OF_TOPICS:
        model = builder.modelBuilder(num_Topic)
        results = []
        results.append(num_Topic)
        with open("testSongList.csv", mode='r', newline='') as songs:
            songReader = csv.reader(songs, delimiter=',', quotechar='"')
            next(songReader, None)
            for song in songReader:
                if song[3] == 'y':
                    trainedSongs.append(song)
                else:
                    untrainedSongs.append(song)

        trainedResults = []
        for pair in combinations(trainedSongs, 2):
            result = runTest(model, pair)
            trainedResults.append(result)
        score = sum(trainedResults)/len(trainedResults)
        results.append(score)
        print("trained finished")

        untrainedResults = []
        for pair in combinations(untrainedSongs, 2):
            result = runTest(model, pair)
            untrainedResults.append(result)
        score = sum(untrainedResults)/len(untrainedResults)
        results.append(score)
        print("untrained finished")

        allSongResults = []
        allSongs = trainedSongs + untrainedSongs
        for pair in combinations(allSongs, 2):
            result = runTest(model, pair)
            allSongResults.append(result)
        score = sum(allSongResults)/len(allSongResults)
        results.append(score)

    with open("outputs/testResults.csv", mode='w', newline='') as results:
        resultsWriter = csv.writer(results, delimiter=',', quotechar='"')
        resultsWriter.writerow(
            ['number of topics', '% trained song comparisons correct', '% untrained song comparisons correct', '% song comparisons correct for all songs'])
        resultsWriter.writerows(results)
