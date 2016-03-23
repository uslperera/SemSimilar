import json

from gensim import models, corpora

from core.model import Document
from core.similarity.main import ss_similarity
from core.textprocessor.tokenize import CodeTokenizer

with open('data/posts.json') as posts_file:
    posts = json.loads(posts_file.read())

Document.set_window(4)
Document.set_tokenizer(CodeTokenizer())
documents = []
for post in posts:
    documents.append(Document(post['Id'], post['Title'], post['Body'], post['Tags']))

# documents = pickle.load(open('temp/documents.p', 'rb'))

texts = []
for doc in documents:
    texts.append(doc.tokens)

dictionary = corpora.Dictionary(texts)
corpus = [dictionary.doc2bow(text) for text in texts]
tfidf = models.TfidfModel(corpus)
tfidf_corpus = tfidf[corpus]

ldamodel = models.ldamodel.LdaModel(tfidf_corpus, id2word=dictionary, num_topics=3)
#ldamodel.save('temp/lda2.model')

# ldamodel = models.LdaModel.load("temp/lda2.model")

with open('data/duplicates.json') as posts_file:
    duplicate_posts = json.loads(posts_file.read())

duplicate_documents = []
for post in duplicate_posts:
    duplicate_documents.append(Document(post['Id'], post['title'], post['body'], post['tags']))

for doc in duplicate_documents:
    results = ss_similarity(lda_model=ldamodel, dictionary=dictionary, corpus=tfidf_corpus, documents=documents,
                            new_document=doc, count=1)
    for top_doc, score in results:
        if top_doc is not None:
            print(doc.id, doc.title, top_doc.id, top_doc.title, score)


