import random
from collections import Counter

'''
def sample_from(weights):
    """returns i with probability weights[i] / sum(weights)"""
    total = sum(weights)
    rnd = total * random.random()
    for i, w in enumerate(weights):
        rnd -= w
        if rnd <= 0:
            return i
    # return the smallest i such that
    # weights[0] + ... + weights[i] >= rnd


documents = [
    ["Hadoop", "Big Data", "HBase", "Java", "Spark", "Storm", "Cassandra"],
    ["NoSQL", "MongoDB", "Cassandra", "HBase", "Postgres"],
    ["Python", "scikit-learn", "scipy", "numpy", "statsmodels", "pandas"],
    ["R", "Python", "statistics", "regression", "probability"],
    ["machine learning", "regression", "decision trees", "libsvm"],
    ["Python", "R", "Java", "C++", "Haskell", "programming languages"],
    ["statistics", "probability", "mathematics", "theory"],
    ["machine learning", "scikit-learn", "Mahout", "neural networks"],
    ["neural networks", "deep learning", "Big Data", "artificial intelligence"],
    ["Hadoop", "Java", "MapReduce", "Big Data"],
    ["statistics", "R", "statsmodels"],
    ["C++", "deep learning", "artificial intelligence", "probability"],
    ["pandas", "R", "Python"],
    ["databases", "HBase", "Postgres", "MySQL", "MongoDB"],
    ["libsvm", "regression", "support vector machines"]
]

K = 4

# a list of Counters, one for each document
document_topic_counts = [Counter() for _ in documents]

# a list of Counters, one for each topic
topic_word_counts = [Counter() for _ in range(K)]

# a list of numbers, one for each topic
topic_counts = [0 for _ in range(K)]

# a list of numbers, one for each document
document_lengths = map(len, documents)

distinct_words = set(word for document in documents for word in document)
W = len(distinct_words)
D = len(documents)


def p_topic_given_document(topic, d, alpha=0.1):
    """the fraction of words in document _d_
    that are assigned to _topic_ (plus some smoothing)"""
    return ((document_topic_counts[d][topic] + alpha) / (document_lengths[d] + K * alpha))


def p_word_given_topic(word, topic, beta=0.1):
    """the fraction of words assigned to _topic_ that equal _word_ (plus some smoothing)"""
    return ((topic_word_counts[topic][word] + beta) / (topic_counts[topic] + W * beta))


def topic_weight(d, word, k):
    """given a document and a word in that document, return the weight for the kth topic"""
    return p_word_given_topic(word, k) * p_topic_given_document(k, d)


def choose_new_topic(d, word):
    return sample_from([topic_weight(d, word, k) for k in range(K)])


random.seed(0)
document_topics = [[random.randrange(K) for word in document]
                   for document in documents]

for d in range(D):
    for word, topic in zip(documents[d], document_topics[d]):
        document_topic_counts[d][topic] += 1
        topic_word_counts[topic][word] += 1
        topic_counts[topic] += 1

for iter in range(1000):
    for d in range(D):
        for i, (word, topic) in enumerate(zip(documents[d], document_topics[d])):
            # remove this word / topic from the counts # so that it doesn't influence the weights document_topic_counts[d][topic] -= 1 topic_word_counts[topic][word] -= 1 topic_counts[topic] -= 1 document_lengths[d] -= 1
            # choose a new topic based on the weights
            new_topic = choose_new_topic(d, word)
            document_topics[d][i] = new_topic
            # and now add it back to the counts
            document_topic_counts[d][new_topic] += 1
            topic_word_counts[new_topic][word] += 1
            topic_counts[new_topic] += 1
            document_lengths[d] += 1

for k, word_counts in enumerate(topic_word_counts):
    for word, count in word_counts.most_common():
        if count > 0:
            print k, word, count
print('-------------')
topic_names = [
    "Big Data and programming languages",
    "Python and statistics",
    "databases",
    "machine learning"]

for document, topic_counts in zip(documents, document_topic_counts):
    print document
    for topic, count in topic_counts.most_common():
        if count > 0:
            print topic_names[topic], count,
            print
'''

# from nltk.metrics import distance
# from scipy.spatial.distance import *
# import numpy as np

# token1 = "Apple"
# token2 = "Apple"

#print distance.jaccard_distance(set(token1), set(token2))

# a = np.asarray(list(token1))
# b = np.asarray(list(token2))
# cosine(np.linalg.norm(token1), np.linalg.norm(token2))
import json

with open('data/100posts.json') as posts_file:
    posts = json.loads(posts_file.read())

new_posts = posts[:1000]

with open('data/test_posts.json', 'w') as file:
    json.dump(new_posts, file)