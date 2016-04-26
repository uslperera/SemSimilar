# from __future__ import division
# import numpy as np
# from semsimilar.model import Document
# from semsimilar.textprocessor.tokenize import CodeTokenizer
# from semsimilar.similarity_core.main import ss_similarity
# from semsimilar.similarity_core.corpus.hal import HAL
# import numpy.linalg as LA
# import scipy.sparse as sp
# from sklearn.feature_extraction.text import TfidfTransformer
# from sklearn.feature_extraction.text import CountVectorizer
#
# from textblob import TextBlob as tb
# import math
#
#
# # def tf(word, blob):
# #     return blob.count(word) / len(blob)
# #
# # def n_containing(word, bloblist):
# #     return sum(1 for blob in bloblist if word in blob)
# #
# # def idf(word, bloblist):
# #     return np.log(len(bloblist) / (1 + n_containing(word, bloblist)))
# #     # return np.log(float(len(bloblist)) / n_containing(word, bloblist)) + 1.0
# #
# # def tfidf(word, blob, bloblist):
# #     return tf(word, blob) * idf(word, bloblist)
#
# # def tf(word, document):
# #     return document.count(word)
# #
# #
# # def df(word, documents):
# #     return sum(1 for document in documents if word in document)
# #
# #
# # def idf(word, document, documents):
# #     return np.log(float(len(documents)) / (df(word, documents) + 1))
# #
# #
# # def tfidf(word, document, documents):
# #     return tf(word, document) * idf(word, document, documents)
#
# def tf(word, document):
#     return document.count(word)
#
#
# def df(word, documents):
#     return sum(1 for document in documents if word in document)
#
#
# def idf(word, document, documents):
#     return np.log(float(len(documents)) / (df(word, documents) + 1))
#
#
# def tfidf(word, document, documents):
#     return tf(word, document) * idf(word, document, documents)
#
#
# if __name__ == '__main__':
#     Document.set_tokenizer(CodeTokenizer())
#
#     docs = ["apple orange",
#             "road apple"]
#
#     documents = []
#     for doc in docs:
#         documents.append(Document(0, doc, None, None))
#
#     texts = []
#     for doc in documents:
#         texts.append(doc.stemmed_tokens)
#
#     # print(texts)
#
#     documents1 = []
#     for doc in documents:
#         documents1.append(" ".join(doc.stemmed_tokens))
#
#     # print(tfidf("orang", documents1[0], documents1))
#
#     dict = {}
#     i = 0
#     for doc in texts:
#         for term in doc:
#             if not dict.has_key(term):
#                 dict[term] = i
#                 i += 1
#
#     # print(dict)
#     dtm = np.zeros((len(texts), len(dict)))
#     for x, doc in enumerate(texts):
#         for term in doc:
#             if dict.has_key(term):
#                 y = dict.get(term)
#                 dtm[x, y] += 1
#
#     # print(dtm)
#     a = TfidfTransformer().fit_transform(dtm)
#     # print(a)
#
#     # print("---")
#     for v in dict:
#         y = dict.get(v)
#         doc_ids = np.where(dtm[:, y] != 0)[0]
#         for x in doc_ids:
#             tf = dtm[x, y]  # term freq.
#             df = len(doc_ids) + 1
#             idf = np.log(float(len(texts)) / df) + 1
#             tfidf = tf * idf
#             dtm[x, y] = LA.norm(tfidf)
#
#     # print(dtm)
#
#     # print("---")
#
#     docA = "apple grape"
#     d = Document(0, docA, "", "")
#     tokens = d.stemmed_tokens
#     s = len(dict)
#     for t in tokens:
#         if not dict.has_key(t):
#             dict[t] = s
#             s += 1
#             new = np.zeros((len(texts), 1))
#             dtm = np.concatenate((dtm, new), axis=1)
#
#     dtm1 = np.zeros((1, len(dict)))
#     for t in tokens:
#         y = dict[t]
#         dtm1[0,y] += 1
#
#     dtm = np.concatenate((dtm, dtm1), axis=0)
#     print(dtm)
#
#     for t in tokens:
#         y = dict[t]
#         doc_ids = np.where(dtm[:, y] != 0)[0]
#         for x in doc_ids:
#             tf = dtm[x, y]  # term freq.
#             df = len(doc_ids) + 1
#             idf = np.log(float(len(texts)) / df) + 1
#             tfidf = tf * idf
#             dtm[x, y] = LA.norm(tfidf)
#
#     print dtm

# import ngram
#
# print ngram.NGram.compare('microsoft', 'Microsoft', N=1)
from nltk.corpus import wordnet as wn
import timeit
a1 = wn.synset('dog.n.01')
a2 = wn.synset('dog.n.01')
start = timeit.default_timer()
print a1.path_similarity(a2)
end = timeit.default_timer()
print(end-start)

#0.000358104705811