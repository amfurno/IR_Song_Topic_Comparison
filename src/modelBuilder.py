from gensim.corpora import Dictionary
from gensim.models import LdaModel
from pprint import pprint

import logging


if __name__ == '__main__':

    logging.basicConfig(
        filename='model.log', format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

    docs = []
    with open('corpus.txt', mode='r') as corpus:
        for line in corpus:
            docs.append(line.split())

    dictionary = Dictionary(docs)
    dictionary.filter_extremes(no_below=10, no_above=0.5)
    corpus = [dictionary.doc2bow(doc) for doc in docs]

    print('Number of unique tokens: %d' % len(dictionary))
    print('Number of documents: %d' % len(corpus))

    # Set training parameters.
    num_topics = 10
    chunksize = 2000
    passes = 30
    iterations = 400
    eval_every = None  # Don't evaluate model perplexity, takes too much time.

# Make a index to word dictionary.
    temp = dictionary[0]  # This is only to "load" the dictionary.
    id2word = dictionary.id2token
    for i in range(20, 100, 10):
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
        avg_topic_coherence = sum([t[1] for t in top_topics]) / num_topics
        print('Average topic coherence for %d topics: %.4f.' % i, avg_topic_coherence)

    top_topics = model.top_topics(corpus)  # , num_words=20)
   
   
