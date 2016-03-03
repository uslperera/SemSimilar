import json
from core.model.document import Document
from core.tokenize import CodeTokenizer
from gensim import corpora, models, matutils
import numpy as np
import scipy.stats as stats
from matplotlib import pyplot as plt

Document.tokenizer(CodeTokenizer())
with open('data/100posts.json') as posts_file:
    posts = json.loads(posts_file.read())

documents = []
for i, post in enumerate(posts):
    if i == 100:
        break
    documents.append(Document(post['Id'], post['Title'], post['Body'], post['Tags']))

texts = []
for doc in documents:
    texts.append(doc.tokens)

dictionary = corpora.Dictionary(texts)
corpus = [dictionary.doc2bow(text) for text in texts]


def sym_kl(p, q):
    return np.sum([stats.entropy(p, q), stats.entropy(q, p)])


l = np.array([sum(cnt for _, cnt in doc) for doc in corpus])


def arun(corpus, dictionary, min_topics=1, max_topics=0, step=1):
    kl = []
    for i in range(min_topics, max_topics, step):
        lda = models.ldamodel.LdaModel(corpus=corpus,
                                       id2word=dictionary, num_topics=i)
        m1 = lda.expElogbeta
        U, cm1, V = np.linalg.svd(m1)
        # Document-topic matrix
        lda_topics = lda[corpus]
        m2 = matutils.corpus2dense(lda_topics, lda.num_topics).transpose()
        cm2 = l.dot(m2)
        cm2 = cm2 + 0.0001
        cm2norm = np.linalg.norm(l)
        cm2 = cm2 / cm2norm
        kl.append(sym_kl(cm1, cm2))
    return kl


kl = arun(corpus, dictionary, max_topics=100)

# Plot kl divergence against number of topics
plt.plot(kl)
plt.ylabel('Symmetric KL Divergence')
plt.xlabel('Number of Topics')
plt.savefig('kldiv.png', bbox_inches='tight')
