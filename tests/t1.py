from core.topicmodel.lda_similarity import similarity as ldasim
from core.main.similarity import similarity as semsim
from gensim import models, corpora
from core.model import Document
from core.tokenize import CodeTokenizer

Document.tokenizer(CodeTokenizer())

docs = ["I like to eat broccoli and bananas.",
        "I ate a banana and spinach smoothie for breakfast.",
        "Chinchillas and kittens are cute.",
        "My sister adopted a kitten yesterday.",
        "Look at this cute hamster munching on a piece of broccoli."]

documents = []
for doc in docs:
    documents.append(Document(0, doc, None, None))

texts = []
for doc in documents:
    texts.append(doc.get_stemmed_tokens())

dictionary = corpora.Dictionary(texts)
corpus = [dictionary.doc2bow(text) for text in texts]
tfidf = models.TfidfModel(corpus)
tfidf_corpus = tfidf[corpus]

print(corpus.__getitem__(2))
# ldamodel = models.ldamodel.LdaModel(tfidf_corpus, id2word=dictionary, num_topics=2)
#
# doc = Document(0, "I prefer to eat broccoli and bananas.", None, None)
# results = ldasim(lda_model=ldamodel, dictionary=dictionary, corpus=tfidf_corpus, documents=documents,
#                  new_document=doc, count=2)
# for top_doc, score in results:
#     if top_doc is not None:
#         print(top_doc.title, score)
#
# print("--------------------------------------------")
# print("--------------------------------------------")
#
# results = semsim(lda_model=ldamodel, dictionary=dictionary, corpus=tfidf_corpus, documents=documents,
#                  new_document=doc, count=2)
# for top_doc, score in results:
#     if top_doc is not None:
#         print(top_doc.title, score)
