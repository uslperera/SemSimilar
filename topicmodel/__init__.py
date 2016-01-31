from gensim import similarities
from model import Result
from textprocessor import Processor


class Similarity(object):
    __lda_model = None
    __documents = None
    __dictionary = None
    __corpus = None
    __count = 1
    __processor = Processor()

    @property
    def count(self):
        return self.__count

    @count.setter
    def count(self, count):
        if count > 0:
            self.__count = count

    def __init__(self, lda_model, dictionary, corpus, documents):
        self.__lda_model = lda_model
        self.__dictionary = dictionary
        self.__documents = documents
        self.__corpus = corpus

    def top(self, document):
        vec_bow = self.__dictionary.doc2bow(document.tokens)
        # convert the query to LDA space
        vec_lda = self.__lda_model[vec_bow]

        index = similarities.MatrixSimilarity(self.__lda_model[self.__corpus])
        index.num_best = self.__count
        sims = index[vec_lda]

        results = []
        for sim in sims:
            result = Result()
            result.score = sim[1]
            result.document = self.__documents[sim[0]]
            results.append(result)

        return results
