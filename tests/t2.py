import json

import pandas

from core.model.document import Document
from core.tokenize import CodeTokenizer
from gensim import models, corpora
from core.topicmodel.lda_similarity import similarity
from matplotlib import pyplot as plt
import numpy as np
from collections import defaultdict

Document.window(4)
Document.tags_enabled = True
Document.description_enabled = True

Document.tokenizer(CodeTokenizer())

count = 20
with open('data/100posts.json') as posts_file:
    posts = json.loads(posts_file.read())

documents = []
for i, post in enumerate(posts):
    if i == count:
        break
    documents.append(Document(post['Id'], post['Title'], post['Body'], post['Tags']))

for document in documents:
    print(document.title, document.tags)

texts = []
for doc in documents:
    texts.append(doc.get_stemmed_tokens())

dictionary = corpora.Dictionary(texts)

corpus = [dictionary.doc2bow(text) for text in texts]

tfidf = models.TfidfModel(corpus)
tfidf_corpus = tfidf[corpus]

# ldamodel = models.ldamodel.LdaModel(tfidf_corpus, id2word=dictionary, num_topics=8)
grid = defaultdict(list)

number_of_words = sum(cnt for document in corpus for _, cnt in document)
parameter_list = range(5, 150, 5)
for parameter_value in parameter_list:
    print "starting pass for parameter_value = %.3f" % parameter_value
    model = models.LdaMulticore(corpus=corpus, workers=None, id2word=dictionary, num_topics=parameter_value,
                                iterations=10)

    perplex = model.bound(corpus)  # this is model perplexity not the per word perplexity
    print "Total Perplexity: %s" % perplex
    grid[parameter_value].append(perplex)

    per_word_perplex = np.exp2(-perplex / number_of_words)
    print "Per-word Perplexity: %s" % per_word_perplex
    grid[parameter_value].append(per_word_perplex)
    # model.save('ldaMulticore_i10_T' + str(parameter_value) + '_training_corpus.lda')
    print

for numtopics in parameter_list:
    print numtopics, '\t', grid[numtopics]

df = pandas.DataFrame(grid)
ax = plt.figure(figsize=(7, 4), dpi=300).add_subplot(111)
df.iloc[1].transpose().plot(ax=ax, color="#254F09")
plt.xlim(parameter_list[0], parameter_list[-1])
plt.ylabel('Perplexity')
plt.xlabel('topics')
plt.title('')
plt.savefig('gensim_multicore_i10_topic_perplexity.pdf', format='pdf', bbox_inches='tight', pad_inches=0.1)
plt.show()
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