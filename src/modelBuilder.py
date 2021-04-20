import csv
import logging
from pprint import pprint

from gensim.corpora import Dictionary
from gensim.models import LdaModel, ldamodel
from gensim.models.coherencemodel import CoherenceModel
from gensim.test.utils import datapath

MODEL_LOCATION = 'outputs/model/model'


def modelBuilder():
    docs = []
    with open('outputs/corpus.txt', mode='r') as lyrics:
        for line in lyrics:
            docs.append(line.split())

    dictionary = Dictionary(docs)
    dictionary.filter_extremes(no_below=20, no_above=0.5)
    corpus = [dictionary.doc2bow(doc) for doc in docs]

    print('Number of unique tokens: %d' % len(dictionary))
    print('Number of documents: %d' % len(corpus))

    # Set training parameters.
    num_topics = 7
    chunksize = 2000
    passes = 10
    iterations = 400
    eval_every = None  # Don't evaluate model perplexity, takes too much time.

# Make a index to word dictionary.
    temp = dictionary[0]  # This is only to "load" the dictionary.
    id2word = dictionary.id2token
    model = LdaModel(
        corpus=corpus,
        id2word=id2word,
        chunksize=chunksize,
        alpha='auto',
        eta='auto',
        iterations=iterations,
        num_topics=num_topics,
        passes=passes,
        eval_every=eval_every
    )
    # Average topic coherence is the sum of topic coherences of all topics, divided by the number of topics.
    coherenceModel = CoherenceModel(
        model=model, texts=docs, dictionary=dictionary, coherence='c_v')

    top_topics = model.top_topics(corpus)  # , num_words=20)
    avg_topic_coherence = sum([t[1] for t in top_topics]) / num_topics
    print('Average UMass topic coherence for %d topics: %.4f.' %
          (num_topics, avg_topic_coherence))
    print('Average C_V topic coherence for %d topics: %.4f.' %
          (num_topics, coherenceModel.get_coherence()))
    return(model)


if __name__ == '__main__':

    logging.basicConfig(
        filename='model.log', format='%(asctime)s : %(levelname)s : %(message)s', level=logging.DEBUG)
    model = modelBuilder()
    model.save(MODEL_LOCATION)
