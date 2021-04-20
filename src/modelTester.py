import modelBuilder as builder
import songComparison as compare

import csv

NUMBER_OF_TOPICS = [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 50, 100, 200, 300, 400]

if __name__ == '__main__':
    modelResults = []
    for num_Topic in NUMBER_OF_TOPICS:
        model = builder.modelBuilder(num_Topic)
        correctResults = 0
        with open("songComparisons.csv", mode='r', newline='') as songs:
            songReader = csv.reader(songs, delimiter=', ', quotechar='"')
            for row in songReader:
                score = compare.songComparison(
                    model, row[0], row[1], row[2], row[3])
                if score >= .65 and row[4] == 1:
                    correctResults += 1
                elif score < .65 and row[4] == 0:
                    correctResults += 1
        modelResults.append([num_Topic, correctResults])

    with open("outputs/testResults.csv", mode='w', newline='') as results:
        resultsWriter = csv.writer(results, delimiter=',', quotechar='"')
        resultsWriter.writerow(
            ['number of topics', 'number of comparisons correct'])
        resultsWriter.writerows(modelResults)
