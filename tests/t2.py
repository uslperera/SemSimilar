#!/usr/bin/python
# -*- coding: utf -*-
#
#  import json
# from collections import defaultdict
#
# import numpy as np
# import pandas
# from gensim import models, corpora
# from matplotlib import pyplot as plt
#
# from semsimilar.model.document import Document
# from semsimilar.textprocessor.tokenize import CodeTokenizer
#
# Document.set_window(4)
# Document.tags_enabled = True
# Document.description_enabled = True
#
# Document.set_tokenizer(CodeTokenizer())
#
# count = 20
# with open('data/100posts.json') as posts_file:
#     posts = json.loads(posts_file.read())
#
# documents = []
# for i, post in enumerate(posts):
#     if i == count:
#         break
#     documents.append(Document(post['Id'], post['Title'], post['Body'], post['Tags']))
#
# for document in documents:
#     print(document.title, document.tags)
#
# texts = []
# for doc in documents:
#     texts.append(doc.get_stemmed_tokens())
#
# dictionary = corpora.Dictionary(texts)
#
# corpus = [dictionary.doc2bow(text) for text in texts]
#
# tfidf = models.TfidfModel(corpus)
# tfidf_corpus = tfidf[corpus]
#
# # ldamodel = models.ldamodel.LdaModel(tfidf_corpus, id2word=dictionary, num_topics=8)
# grid = defaultdict(list)
#
# number_of_words = sum(cnt for document in corpus for _, cnt in document)
# parameter_list = range(5, 150, 5)
# for parameter_value in parameter_list:
#     print "starting pass for parameter_value = %.3f" % parameter_value
#     model = models.LdaMulticore(corpus=corpus, workers=None, id2word=dictionary, num_topics=parameter_value,
#                                 iterations=10)
#
#     perplex = model.bound(corpus)  # this is model perplexity not the per word perplexity
#     print "Total Perplexity: %s" % perplex
#     grid[parameter_value].append(perplex)
#
#     per_word_perplex = np.exp2(-perplex / number_of_words)
#     print "Per-word Perplexity: %s" % per_word_perplex
#     grid[parameter_value].append(per_word_perplex)
#     # model.save('ldaMulticore_i10_T' + str(parameter_value) + '_training_corpus.lda')
#     print
#
# for numtopics in parameter_list:
#     print numtopics, '\t', grid[numtopics]
#
# df = pandas.DataFrame(grid)
# ax = plt.figure(figsize=(7, 4), dpi=300).add_subplot(111)
# df.iloc[1].transpose().plot(ax=ax, color="#254F09")
# plt.xlim(parameter_list[0], parameter_list[-1])
# plt.ylabel('Perplexity')
# plt.xlabel('topics')
# plt.title('')
# plt.savefig('gensim_multicore_i10_topic_perplexity.pdf', format='pdf', bbox_inches='tight', pad_inches=0.1)
# plt.show()
# df.to_pickle('gensim_multicore_i10_topic_perplexity.df')

# print("...............")
# while True:
#     title = raw_input("> ")
#     doc = Document(0, title, None, None)
#     results = similarity(lda_model=ldamodel, dictionary=dictionary, corpus=tfidf_corpus, documents=documents,
#                          new_document=doc, count=1)
#     top_doc, score = results[0]
#     print(top_doc.title, score)
#     print("----------------------------")

# for i, post in enumerate(posts):
#     if i > count:
#         doc = Document(post['Id'], post['Title'], post['Body'], post['Tags'])
#         results = similarity(lda_model=ldamodel, dictionary=dictionary, corpus=tfidf_corpus, documents=documents,
#                              new_document=doc, count=1)
#         top_doc, score = results[0]
#         print(i, doc.tags, doc.title, top_doc.title, score)
#         print("----------------------------")
#         raw_input("Continue > ")

# as_int = x.astype(int)
# print(as_int)
# as_int.
# print(np.cross(x, x, axis=1))

from semsimilar.textprocessor.tokenize import CodeTokenizer
from semsimilar.textprocessor.processor import *
from semsimilar.model.document import Document
from semsimilar.similarity_core.corpus.hal import HAL
from semsimilar.similarity_core.knowledge.lesk import similarity

# c = CodeTokenizer()
# Document.set_tokenizer(c)
# # ["he tried to break the bank at Monte Carlo", "he sat on the bank of the river and watched the currents"]
# documents = [Document(1, "he tried to break the bank at Monte Carlo", None, None),
#              Document(2, "he sat on the bank of the river and watched the currents", None, None)]
#
# text = []
# for doc in documents:
#     text.append(" ".join(doc.stemmed_tokens))
#
# h = HAL(text)
#
# query_document = Document(0, None, None, None)
#
# # results = h.semantic_search(query_document.stemmed_tokens)
# results = similarity(documents, query_document, 2)
# print(results[0][0].id)
# print(results[1][0].id)

# import numpy as np
# import numpy.linalg as LA
# from scipy.spatial import distance
#
# def cosine(a, b):
#     # Find the cosine distance between two vectors
#     try:
#         result = round(np.inner(a, b) / (LA.norm(a) * LA.norm(b)), 3)
#     except ZeroDivisionError:
#         result = 0
#     return result
#
# a = np.array([(1, 0, 1, 1)])
# b = np.array([(1, 0, 0, 1)])
# print(1-distance.cosine(a, b))
# print(cosine(a,b))

import json
import httplib, urllib
from StringIO import StringIO

params = urllib.urlencode({'wt': "json", 'indent': 'true', 'q': 'police'})
headers = {"Content-type": "application/x-www-form-urlencoded",
            "Accept": "text/plain"}
conn = httplib.HTTPConnection("localhost", 8983)
conn.request("GET", "/solr/gettingstarted/select", params, headers)
response = conn.getresponse()
print response.status, response.reason
data = response.read()
print(data)
io = StringIO(data)
res = json.load(io)
for obj in res["response"]["docs"]:
    print(int(obj["Id"]))

# post_links = {}
#
# def load_post_links():
#     with open('data/1000ids.json') as postlinks_file:
#         postlinks = json.loads(postlinks_file.read())
#
#     for i, p in enumerate(postlinks):
#         if not post_links.has_key(int(p['PostId'])):
#             post_links[int(p['PostId'])] = int(p['RelatedPostId'])
#         elif isinstance(post_links[int(p['PostId'])], list):
#             post_links[int(p['PostId'])].append(int(p['RelatedPostId']))
#         else:
#             temp = post_links[int(p['PostId'])]
#             post_links[int(p['PostId'])] = [temp]
#             post_links[int(p['PostId'])].append(int(p['RelatedPostId']))
#
# def search_post_link(dup_p, ori_p):
#     for plink in post_links:
#         dp, op = plink
#         if op == int(ori_p) and dp == int(dup_p):
#             return True
#     return False
#
# load_post_links()
#
# documents = {}
# with open('data/100posts.json') as posts:
#     posts = json.loads(posts.read())
#
#     for i, p in enumerate(posts):
#         if i == 1000:
#             break
#         documents[int(p['Id'])]=p['Title']
#
# with open('data/100duplicates.json') as posts_file:
#     duplicate_posts = json.loads(posts_file.read())
#
#     duplicate_documents = []
#     for i, post in enumerate(duplicate_posts):
#         if i == 1000:
#             break
#         if post_links.has_key(int(post['Id'])):
#             original_post_id = post_links[int(post['Id'])]
#             if isinstance(original_post_id, list):
#                 original_post_id = int(original_post_id[0])
#             if documents.has_key(original_post_id):
#                 title = documents[original_post_id]
#                 print original_post_id, title, int(post['Id']), post['Title']
