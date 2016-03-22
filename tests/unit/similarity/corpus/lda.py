import unittest

from gensim import corpora, models, similarities
from mock.mock import MagicMock, patch

from core.model.document import Document
from core.similarity.corpus import lda as lda
from core.textprocessor.tokenize import CodeTokenizer


class LDAResultsTestCase(unittest.TestCase):
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
            texts.append(document.stemmed_tokens)

        # convert all the documents to a matrix
        cls.dictionary = corpora.Dictionary(texts)
        cls.corpus = [cls.dictionary.doc2bow(text) for text in texts]

        # generate LDA model
        # Topics are health, food, motor
        cls.ldamodel = models.ldamodel.LdaModel(cls.corpus, num_topics=3, id2word=cls.dictionary, passes=20)

    @patch('core.model.document.Document.generate_tokens', MagicMock())
    @patch('core.model.document.Document.get_stemmed_tokens', MagicMock())
    @patch('gensim.corpora.Dictionary.doc2bow', MagicMock())
    def test_matched_result(self):
        """If a document is matched"""
        expected_doc = self.documents[1]

        new_document = Document(0, "Brocolli is a good vegetable for health", "", "Health, Food")

        # Set the result
        similarities.MatrixSimilarity.__getitem__ = MagicMock(return_value=[(1, 0.99770945310592651)])

        # Get the most similar document
        results = lda.similarity(lda_model=self.ldamodel, dictionary=self.dictionary, corpus=self.corpus,
                                 documents=self.documents,
                                 new_document=new_document, count=1)

        top_doc, score = results[0]
        self.assertEqual(top_doc.id, expected_doc.id)

    @patch('core.model.document.Document.generate_tokens', MagicMock())
    @patch('core.model.document.Document.get_stemmed_tokens', MagicMock())
    @patch('gensim.corpora.Dictionary.doc2bow', MagicMock())
    def test_unmatched_result(self):
        """If no documents are matched"""
        expected_result = 0

        new_document = Document(0, "NASA announced plans to send a manned mission to Mars in the 2030", "", "Science")

        # set the result
        similarities.MatrixSimilarity.__getitem__ = MagicMock(return_value=[])

        # Get the most similar document
        results = lda.similarity(lda_model=self.ldamodel, dictionary=self.dictionary, corpus=self.corpus,
                                 documents=self.documents,
                                 new_document=new_document, count=1)

        self.assertEqual(len(results), expected_result)


class LDAResultsCountTestCase(unittest.TestCase):
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
            texts.append(document.stemmed_tokens)

        # convert all the documents to a matrix
        cls.dictionary = corpora.Dictionary(texts)
        cls.corpus = [cls.dictionary.doc2bow(text) for text in texts]

        # generate LDA model
        # Topics are health, food, motor
        cls.ldamodel = models.ldamodel.LdaModel(cls.corpus, num_topics=3, id2word=cls.dictionary, passes=20)

    @patch('core.model.document.Document.generate_tokens', MagicMock())
    @patch('core.model.document.Document.get_stemmed_tokens', MagicMock())
    @patch('gensim.corpora.Dictionary.doc2bow', MagicMock())
    def test_invalid_count(self):
        """If an invalid count is given"""
        expected_count = 1

        new_document = Document(0, "Brocolli is a good vegetable for health", "", "Health, Food")

        # Set the results to be returned
        similarities.MatrixSimilarity.__getitem__ = MagicMock(
                return_value=[(1, 0.99770945310592651)])

        # Get the most similar document
        results = lda.similarity(lda_model=self.ldamodel, dictionary=self.dictionary, corpus=self.corpus,
                                 documents=self.documents,
                                 new_document=new_document, count=0)

        self.assertEqual(len(results), expected_count)

    @patch('core.model.document.Document.generate_tokens', MagicMock())
    @patch('core.model.document.Document.get_stemmed_tokens', MagicMock())
    @patch('gensim.corpora.Dictionary.doc2bow', MagicMock())
    def test_valid_count(self):
        """If a valid count is given"""
        expected_count = 2

        new_document = Document(0, "Brocolli is a good vegetable for health", "", "Health, Food")

        # Set the results to be returned
        similarities.MatrixSimilarity.__getitem__ = MagicMock(
                return_value=[(1, 0.99770945310592651), (0, 0.89770945310592651)])

        # Get the most similar documents
        results = lda.similarity(lda_model=self.ldamodel, dictionary=self.dictionary, corpus=self.corpus,
                                 documents=self.documents,
                                 new_document=new_document, count=expected_count)

        self.assertEqual(len(results), expected_count)
