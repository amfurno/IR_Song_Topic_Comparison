from gensim.corpora import Dictionary
from gensim.models import LdaModel
from gensim.models.coherencemodel import CoherenceModel
from nltk.corpus import stopwords
from pprint import pprint
import logging
import csv

if __name__ == '__main__':

    logging.basicConfig(
        filename='model.log', format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

    docs = []
    with open('outputs/corpus.txt', mode='r') as lyrics:
        for line in lyrics:
            docs.append(line.split())

    dictionary = Dictionary(docs)
    dictionary.filter_extremes(no_below=10, no_above=0.5)
    corpus = [dictionary.doc2bow(doc) for doc in docs]

    print('Number of unique tokens: %d' % len(dictionary))
    print('Number of documents: %d' % len(corpus))

    # Set training parameters.
    num_topics = 10
    chunksize = 2000
    passes = 50
    iterations = 400
    eval_every = None  # Don't evaluate model perplexity, takes too much time.

# Make a index to word dictionary.
    temp = dictionary[0]  # This is only to "load" the dictionary.
    id2word = dictionary.id2token
    with open("outputs/topicCoherence.csv", mode='a', newline='') as coherenceCSV:

        coherenceWriter = csv.writer(
            coherenceCSV, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        coherenceWriter.writerow(
            ['Number of topics', 'coherence model value', 'avg topic coherence'])

        for i in range(200, 401, 20):
            model = LdaModel(
                corpus=corpus,
                id2word=id2word,
                chunksize=chunksize,
                alpha='auto',
                eta='auto',
                iterations=iterations,
                num_topics=i,
                passes=passes,
                eval_every=eval_every
            )
            # Average topic coherence is the sum of topic coherences of all topics, divided by the number of topics.
            coherenceModel = CoherenceModel(
                model=model, texts=docs, dictionary=dictionary, coherence='c_v')
            top_topics = model.top_topics(corpus)  # , num_words=20)
            avg_topic_coherence = sum([t[1] for t in top_topics]) / i
            coherenceWriter.writerow(
                [i, coherenceModel.get_coherence(), avg_topic_coherence])
            print('Average topic coherence for %d topics: %.4f.' %
                  (i, avg_topic_coherence))
