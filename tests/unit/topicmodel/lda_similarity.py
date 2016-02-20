import unittest
from core.textprocessor.synsets import process
from core.model.document import Document
from gensim import corpora, models
from core.topicmodel import lda_similarity as lda


class LDATestCase(unittest.TestCase):
    doc_a = "Brocolli is good to eat. My brother likes to eat good brocolli, but not my mother."
    doc_b = "My mother spends a lot of time driving my brother around to baseball practice."
    doc_c = "Some health experts suggest that driving may cause increased tension and blood pressure."
    doc_d = "I often feel pressure to perform well at school, but my mother never seems to drive my brother to do better."
    doc_e = "Health professionals say that brocolli is good for your health."
    doc_f = "lawyer"

    # compile sample documents into a list
    doc_set = [doc_a, doc_b, doc_c, doc_d, doc_e, doc_f]

    def test(self):
        #duplicate_documents = [Document(0, "Brocolli is a good vegetable for health", "", "")]
        duplicate_documents = [Document(0, "attorney", "", "")]
        documents = []
        for doc in self.doc_set:
            documents.append(Document(0, doc, "", ""))

        process(documents, True, False, False, 0)

        process(duplicate_documents, True, False, False, 0)

        texts = []
        for document in documents:
            texts.append(document.tokens)

        dictionary = corpora.Dictionary(texts)
        corpus = [dictionary.doc2bow(text) for text in texts]

        # generate LDA model
        ldamodel = models.ldamodel.LdaModel(corpus, num_topics=3, id2word=dictionary, passes=20)

        results = lda.similarity(lda_model=ldamodel, dictionary=dictionary, corpus=corpus, documents=documents,
                                 new_document=duplicate_documents[0], count=2)
        for top_doc, score in results:
            if top_doc is not None:
                print(top_doc.title, score)
