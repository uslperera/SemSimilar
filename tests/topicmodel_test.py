from gensim import models, corpora
import json
from core.model import Document
from core.textprocessor.document_builder import process
from core.topicmodel import lda_similarity as lda

with open('data/posts2.json') as posts_file:
    posts = json.loads(posts_file.read())

documents = []
for post in posts:
    documents.append(Document(post['Id'], post['Title'], post['Body'], post['Tags']))

process(documents=documents, title_enabled=True, description_enabled=False, tags_enabled=True, window=0)

texts = []
for doc in documents:
    texts.append(doc.tokens)

dictionary = corpora.Dictionary(texts)
corpus = [dictionary.doc2bow(text) for text in texts]
tfidf = models.TfidfModel(corpus)
tfidf_corpus = tfidf[corpus]

ldamodel = models.ldamodel.LdaModel(tfidf_corpus, id2word = dictionary, num_topics=100)
#ldamodel.save('temp/lda1.model')

#ldamodel = models.LdaModel.load("temp/lda2.model")

with open('data/duplicates.json') as posts_file:
    duplicate_posts = json.loads(posts_file.read())

duplicate_documents = []
for post in duplicate_posts:
    duplicate_documents.append(Document(post['Id'], post['title'], post['body'], post['tags']))

process(documents=duplicate_documents, title_enabled=True, description_enabled=False, tags_enabled=True, window=0)

for doc in duplicate_documents:
    results = lda.similarity(lda_model=ldamodel, dictionary=dictionary, corpus=tfidf_corpus, documents=documents,
                             new_document=doc, count=1)
    for top_doc, score in results:
        if top_doc is not None:
            print(doc.id, doc.title, top_doc.id, top_doc.title, score)