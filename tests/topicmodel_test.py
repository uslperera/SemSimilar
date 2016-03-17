import json

from gensim import models, corpora

from core.model import Document
from core.similarity.corpus import lda as lda
from core.textprocessor.tokenize import CodeTokenizer

Document.set_tokenizer(CodeTokenizer())

# Read all the documents from the data source
posts = []
with open('data/100posts.json') as posts_file:
    posts = json.loads(posts_file.read())

documents = []
for i, post in enumerate(posts):
    if i == 10:
        break
    print(post['Title'])
    documents.append(Document(post['Id'], post['Title'], post['Body'], post['Tags']))

texts = []
for doc in documents:
    texts.append(doc.tokens)

dictionary = corpora.Dictionary(texts)
corpus = [dictionary.doc2bow(text) for text in texts]

# __tfidf = models.TfidfModel(corpus)
# tfidf_corpus = __tfidf[corpus]

ldamodel = models.ldamodel.LdaModel(corpus, id2word=dictionary, num_topics=8)
# ldamodel = models.ldamodel.LdaModel(tfidf_corpus, id2word=dictionary, num_topics=8)
# ldamodel.save('temp/lda1.model')

# ldamodel = models.LdaModel.load("temp/lda2.model")

# with open('data/duplicates.json') as posts_file:
#     duplicate_posts = json.loads(posts_file.read())
#
# duplicate_documents = []
# for post in duplicate_posts:
#     duplicate_documents.append(Document(post['Id'], post['title'], post['body'], post['tags']))
#
# process(documents=duplicate_documents, title_enabled=True, description_enabled=False, tags_enabled=True, set_window=0)

d = Document(0, "How do I calculate someone's age in C#", "", "")
duplicate_documents = [d]

for doc in duplicate_documents:
    results = lda.similarity(lda_model=ldamodel, dictionary=dictionary, corpus=corpus, documents=documents,
                             new_document=doc, count=1)
    for top_doc, score in results:
        if top_doc is not None:
            print(doc.id, doc.title, top_doc.id, top_doc.title, score)
