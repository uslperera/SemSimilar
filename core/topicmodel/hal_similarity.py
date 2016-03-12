import numpy.linalg as LA
from scipy.sparse import csr_matrix
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer, TfidfVectorizer
from scipy.spatial.distance import *


class HAL(object):
    count_vectorizer = None
    dtm = None
    wwm = None
    dist = None
    threshold = 0.1
    vocabulary = None

    def __init__(self, documents):
        # self.count_vectorizer = CountVectorizer(input="content")
        self.count_vectorizer = TfidfVectorizer(input="content")
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

        dtm2 = np.append(self.dtm.toarray(), dtm1.toarray(), axis=0)
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
