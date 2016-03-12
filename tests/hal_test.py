import numpy.linalg as LA
from scipy.sparse import csr_matrix
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
import numpy as np
from nltk.metrics.association import BigramAssocMeasures
from scipy.spatial.distance import *

from sklearn.metrics.pairwise import cosine_similarity
from itertools import izip

# docs = ["I like to eat broccoli and bananas.",
#         "I ate a banana and spinach smoothie for breakfast.",
#         "Chinchillas and kittens are cute.",
#         "My sister adopted a kitten yesterday.",
#         "Look at this cute hamster munching on a piece of broccoli."]
docs = ["lawyer courthouse",
        "ate banana morning",
        "attorney came courthouse"]

c = CountVectorizer(input="content", stop_words="english")
dtm = c.fit_transform(docs)
# print(dtm)
# print("-----------------------")
vocabulary = c.get_feature_names()
v = np.array(vocabulary)


# new_doc = ["banana", "good", "eat", "breakfast"]
# c = []
# for term in new_doc:
#     i = np.where(v == term)[0]
#     if len(i) > 0:
#         c.append(i[0])
#
# print(c)
# similar_docs = []
# for c1 in c:
#     similar_docs.extend(np.where(dtm[:, c1] == 1)[0])
#
# similar = set(similar_docs)
#
#
# for s in similar:
#     print(dtm[s])
#
# print("----")
def add_document():
    query = "banana is good to eat after breakfast"

    """convert the query into dtm using existing vocab"""

    count = CountVectorizer(input="content", stop_words="english", vocabulary=vocabulary)
    dtm1 = count.fit_transform([query])
    print(dtm1)
    dtm2 = np.append(dtm.toarray(), dtm1.toarray(), axis=0)
    A = csr_matrix(dtm2)
    print(A)
    print("--")
    print(dtm.toarray())
    print("--")
    print(dtm1.toarray())
    print("--")
    print(A.toarray())


def sim():
    threshold = 0.1
    query = "banana is good to eat after breakfast"

    """convert the query into dtm using existing vocab"""

    count = CountVectorizer(input="content", stop_words="english", vocabulary=vocabulary)
    dtm1 = count.fit_transform([query])

    cx = lambda a, b: round(np.inner(a, b) / (LA.norm(a) * LA.norm(b)), 3)

    new_doc = ["banana", "good", "eat", "breakfast", "after"]
    c = []
    for term in new_doc:
        i = np.where(v == term)[0]
        if len(i) > 0:
            c.append(i[0])

    similar_docs = []
    d = dtm.toarray()
    for c1 in c:
        similar_docs.extend(np.where(d[:, c1] == 1)[0])

    similar = set(similar_docs)

    results = []
    for s in similar:
        cosine = cx(dtm1.toarray(), d[s])
        if cosine > threshold:
            doc = (s, cosine)
            results.append(doc)

    results.sort(key=lambda tup: tup[1], reverse=True)
    print(results)


def tes():
    train_set = ["The sky is blue.", "The sun is bright."]  # Documents
    test_set = ["The sun in the sky is bright."]  # Query

    vectorizer = CountVectorizer(stop_words='english')
    # print vectorizer
    transformer = TfidfTransformer()
    # print transformer

    trainVectorizerArray = vectorizer.fit_transform(train_set).toarray()
    testVectorizerArray = vectorizer.transform(test_set).toarray()
    print 'Fit Vectorizer to train set', trainVectorizerArray
    print 'Transform Vectorizer to test set', testVectorizerArray
    cx = lambda a, b: round(np.inner(a, b) / (LA.norm(a) * LA.norm(b)), 3)

    for vector in trainVectorizerArray:
        print vector
        for testV in testVectorizerArray:
            print testV
            cosine = cx(vector, testV)
            print cosine

    transformer.fit(trainVectorizerArray)
    print
    print transformer.transform(trainVectorizerArray).toarray()

    transformer.fit(testVectorizerArray)
    print
    tfidf = transformer.transform(testVectorizerArray)
    print tfidf.todense()


def convertPPMI(mat):
    """
     Compute the PPMI values for the raw co-occurrence matrix.
     PPMI values will be written to mat and it will get overwritten.
     """
    (nrows, ncols) = mat.shape
    print "no. of rows =", nrows
    print "no. of cols =", ncols
    colTotals = mat.sum(axis=0)
    rowTotals = mat.sum(axis=1).T
    N = np.sum(rowTotals)
    rowMat = np.ones((nrows, ncols), dtype=np.float)
    for i in range(nrows):
        rowMat[i, :] = 0 if rowTotals[0, i] == 0 else rowMat[i, :] * (1.0 / rowTotals[0, i])
    colMat = np.ones((nrows, ncols), dtype=np.float)
    for j in range(ncols):
        colMat[:, j] = 0 if colTotals[0, j] == 0 else (1.0 / colTotals[0, j])
    P = N * mat.toarray() * rowMat * colMat
    P = np.fmax(np.zeros((nrows, ncols), dtype=np.float64), np.log(P))
    return csr_matrix(P)


class HAL(object):
    count_vectorizer = None
    dtm = None
    wwm = None
    dist = None
    threshold = 0.1
    vocabulary = None

    def __init__(self, documents):
        self.count_vectorizer = CountVectorizer(input="content")
        self.dtm = self.count_vectorizer.fit_transform(documents)
        self.vocabulary = np.array(self.count_vectorizer.get_feature_names())
        self.create_word_to_word_matrix(documents)

    def cosine(self, a, b):
        if (LA.norm(a) * LA.norm(b)) != 0:
            return round(np.inner(a, b) / (LA.norm(a) * LA.norm(b)), 3)
        return 0

    def create_word_to_word_matrix(self, documents):
        l = len(self.vocabulary)
        self.wwm = np.zeros((l, l), dtype=np.float)

        for doc in documents:
            tokens = doc.split(" ")
            for f_token in tokens:
                term_id = self.get_term_id(f_token)
                if term_id is not None:
                    for token in tokens:
                        x = self.get_term_id(token)
                        if x is not None:
                            self.wwm[term_id, x] = 1

                            # self.dist = cosine_similarity(dtm)
        wwm = np.zeros((l, l), dtype=np.float)
        for y, v in enumerate(self.vocabulary):
            for x, v in enumerate(self.vocabulary):
                score = self.cosine(self.wwm[:, x], self.wwm[:, y])
                wwm[x, y] = score
        self.wwm = wwm

    def add_document(self, document):
        count = CountVectorizer(input="content", stop_words="english", vocabulary=self.vocabulary)
        dtm1 = count.fit_transform([" ".join(document)])

        dtm2 = np.append(dtm.toarray(), dtm1.toarray(), axis=0)
        self.dtm = csr_matrix(dtm2)

    def get_related_vocabulary(self, query):
        word_ids = []
        for term in query:
            term_id = np.where(self.vocabulary == term)[0]
            if len(term_id) > 0:
                id = term_id[0]
                for i, score in enumerate(self.wwm[id, :]):
                    if score > 0.4:
                        word_ids.append(i)
        return word_ids

    def search(self, query):
        countVectorizer = CountVectorizer(input="content", stop_words="english",
                                          vocabulary=self.count_vectorizer.get_feature_names())
        query_string = " ".join(query)
        qtm = countVectorizer.fit_transform([query_string]).toarray()

        dtm = self.dtm.toarray()

        term_ids = []
        for term in query:
            term_id = self.get_term_id(term)
            if term_id is not None:
                term_ids.append(term_id)

        similar_docs = []
        for term_id in term_ids:
            similar_docs.extend(np.where(dtm[:, term_id] != 0)[0])

        similar = set(similar_docs)

        results = []
        for s in similar:
            cos = self.cosine(qtm, dtm[s])
            # cos = 1 - cosine(qtm, dtm[s])
            if cos > self.threshold:
                doc = (s, cos)
                results.append(doc)

        """"""
        semantic_term_ids = set(self.get_related_vocabulary(query))
        se_doc_ids = []
        for term_id in semantic_term_ids:
            doc = np.where(dtm[:, term_id] != 0)[0][0]
            se_doc_ids.append(doc)

        for s in (set(se_doc_ids) - similar):
            doc = (s, 0)
            results.append(doc)
        """"""

        results.sort(key=lambda tup: tup[1], reverse=True)
        return results

    def get_term_id(self, term):
        term_id = np.where(self.vocabulary == term)[0]
        if len(term_id) > 0:
            return term_id[0]
        return None


if __name__ == '__main__':
    print("--test--")
    # sim()
    # h = HAL(documents=docs)
    # new_doc = ["banana", "good", "eat", "breakfast", "after"]
    # r = h.search(new_doc)
    # # print(r)
    # print(h.count_vectorizer.vocabulary_)
    # print(len(h.count_vectorizer.vocabulary_))
    # h.count_vectorizer.vocabulary_["shamal"] = len(h.count_vectorizer.vocabulary_)
    #
    # print(h.count_vectorizer.vocabulary_)
    # print(h.count_vectorizer.get_feature_names())
    # print(vocabulary)

    h = HAL(documents=docs)
    print(h.wwm)
    new_doc = ["lawyer", "arrived", "place"]
    r = h.search(new_doc, 2)
    print(r)

    # print(vocabulary)
    # l = len(vocabulary)
    # wwm = np.zeros((l, l), dtype=np.float)
    #
    # for doc in docs:
    #     tokens = doc.lower().split(" ")
    #     for f_token in tokens:
    #         term_id = np.where(v == f_token)[0][0]
    #         for token in tokens:
    #             x = np.where(v == token)[0][0]
    #             wwm[term_id, x] = 1
    #
    # print(wwm)
    #
    # cx = lambda a, b: round(np.inner(a, b) / (LA.norm(a) * LA.norm(b)), 3)
    #
    # word_ids = []
    # new_doc = ["lawyer", "arrived", "place"]
    # for term in new_doc:
    #     term_id = np.where(v == term)[0]
    #     if len(term_id) > 0:
    #         id = term_id[0]
    #         for i, ve in enumerate(wwm):
    #             score = cx(wwm[:, id], ve)
    #             if score > 0.4:
    #                 word_ids.append(i)
    #
    # print(word_ids)
