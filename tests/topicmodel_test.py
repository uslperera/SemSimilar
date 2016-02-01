from gensim import models, corpora
import json
from core.model import Document, Result
from core.textprocessor import DocumentsBuilder
from core.topicmodel import Similarity

with open('data/posts1.json') as posts_file:
    posts = json.loads(posts_file.read())

documents = []
for post in posts:
    documents.append(Document(post['Id'], post['Title'], post['Body'], post['Tags']))

docs_builder = DocumentsBuilder(documents)
docs_builder.tags_enabled = True
#docs_builder.description_enabled = True
docs_builder.process()

texts = []
for doc in documents:
    texts.append(doc.tokens)

dictionary = corpora.Dictionary(texts)
corpus = [dictionary.doc2bow(text) for text in texts]
tfidf = models.TfidfModel(corpus)
tfidf_corpus = tfidf[corpus]

#ldamodel = models.ldamodel.LdaModel(tfidf_corpus, id2word = dictionary, num_topics=90)
#ldamodel.save('temp/lda1.model')

ldamodel = models.LdaModel.load("temp/lda1.model")

s = Similarity(lda_model=ldamodel, dictionary=dictionary, corpus=tfidf_corpus, documents=documents)
s.count = 2

with open('data/duplicates1.json') as posts_file:
    duplicate_posts = json.loads(posts_file.read())

duplicate_documents = []
for post in duplicate_posts:
    duplicate_documents.append(Document(post['Id'], post['title'], post['body'], post['tags']))

new_docs_builder = DocumentsBuilder(duplicate_documents)
new_docs_builder.tags_enabled = True
#new_docs_builder.description_enabled = True
new_docs_builder.process()

for doc in duplicate_documents:
    results = s.top(doc)
    for result in results:
        top_doc = result.document
        if top_doc is not None:
            print(doc.id, doc.title, top_doc.id, top_doc.title, result.score)
