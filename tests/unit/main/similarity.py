import unittest

from gensim import corpora, models
from mock.mock import patch

from core.main import similarity
from core.model.document import Document
from core.textprocessor.tokenize import CodeTokenizer


class SimilarityTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        Document.set_tokenizer(CodeTokenizer())
        doc_a = Document(1, "Some health experts suggest that driving may cause increased tension and blood pressure.",
                         "",
                         "Health, Motor")
        doc_b = Document(2, "Health professionals say that brocolli is good for your health.", "", "Health, Food")

        # compile sample documents into a list
        cls.documents = [doc_a, doc_b]
        texts = []
        for document in cls.documents:
            texts.append(document.get_stemmed_tokens())

        # convert all the documents to a matrix
        cls.dictionary = corpora.Dictionary(texts)
        cls.corpus = [cls.dictionary.doc2bow(text) for text in texts]

        # generate LDA model
        # Topics are health, food, motor
        cls.ldamodel = models.ldamodel.LdaModel(cls.corpus, num_topics=3, id2word=cls.dictionary, passes=20)

    @patch('core.knowledge.lesk_similarity.similarity')
    @patch('core.corpus.lda_similarity.similarity')
    def test_similarity(self, lda, lesk):
        """Check for similarity"""
        expected_document = self.documents[0]
        expected_score = 1.0

        lda.return_value = [(self.documents[1], 0.989899), (self.documents[0], 0.70009)]
        lesk.return_value = [(self.documents[0], 1.0), (self.documents[1], 0.890909)]

        new_document = Document(0, "Brocolli is a good vegetable for health", "", "Health, Food")
        results = similarity(self.documents, new_document, 1, self.ldamodel, self.dictionary, self.corpus)
        top_doc, score = results[0]

        self.assertEqual(top_doc.id, expected_document.id)
        self.assertEqual(score, expected_score)
