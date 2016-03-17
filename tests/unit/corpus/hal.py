import unittest
from mock.mock import MagicMock, patch
from sklearn.feature_extraction import text
from core.similarity.corpus.hal import *
from core.model.document import Document
from core.textprocessor.tokenize import CodeTokenizer
import numpy as np


class HALVocabularyTestCase(unittest.TestCase):
    @patch('core.similarity.corpus.hal.HAL.create_word_to_word_matrix', MagicMock())
    def test(self):
        # vocab after stemming
        expected_vocab = [u'test']

        Document.set_tokenizer(CodeTokenizer())
        documents = []
        documents.append(Document(1, "test", "", ""))
        texts = []

        for doc in documents:
            texts.append(" ".join(doc.get_stemmed_tokens()))
        # HAL.create_word_to_word_matrix = MagicMock()
        h = HAL(texts)
        self.assertEqual(str(h.vocabulary), str(expected_vocab))


class HALDTMatrixTestCase(unittest.TestCase):
    @patch('core.similarity.corpus.hal.HAL.create_word_to_word_matrix', MagicMock())
    def test(self):
        expected_dtm = "[[ 0.  0.  1.]\n [ 1.  0.  0.]\n [ 0.  1.  0.]]"

        Document.set_tokenizer(CodeTokenizer())
        documents = []
        documents.append(Document(1, "test", "", ""))
        documents.append(Document(2, "document", "", ""))
        documents.append(Document(3, "matrix", "", ""))
        texts = []

        for doc in documents:
            texts.append(" ".join(doc.get_stemmed_tokens()))
        # HAL.create_word_to_word_matrix = MagicMock()
        h = HAL(texts)
        self.assertEqual(h.document_term_matrix.toarray().__str__(), expected_dtm)


class HALWTWMatrixTestCase(unittest.TestCase):
    def test(self):
        expected_dtm = "[[ 1.  0.]\n [ 0.  1.]]"

        Document.set_tokenizer(CodeTokenizer())
        documents = []
        documents.append(Document(1, "word to word", "", ""))
        documents.append(Document(2, "matrix", "", ""))
        texts = []

        for doc in documents:
            texts.append(" ".join(doc.get_stemmed_tokens()))
        h = HAL(texts)
        self.assertEqual(h.word_word_matrix.__str__(), expected_dtm)


class HALCosineTestCase(unittest.TestCase):
    def test(self):
        a = np.array([1, 1, 0, 1])
        b = np.array([1, 1, 0, 1])
        score = HAL.cosine(a, b)
        self.assertEqual(score, 1)


class HALDTMatrixTestCase(unittest.TestCase):
    @patch('core.similarity.corpus.hal.HAL.create_word_to_word_matrix', MagicMock())
    def test(self):
        expected_dtm = np.array([(0, 1), (1, 0), (1, 1)])

        Document.set_tokenizer(CodeTokenizer())
        documents = []
        documents.append(Document(1, "test", "", ""))
        documents.append(Document(2, "document", "", ""))
        texts = []

        for doc in documents:
            texts.append(" ".join(doc.get_stemmed_tokens()))
        # HAL.create_word_to_word_matrix = MagicMock()
        h = HAL(texts)
        h.add_document(Document(3, "test document", "", "").get_stemmed_tokens())
        self.assertTrue(np.array_equal(h.document_term_matrix.toarray(), expected_dtm))


class HALTermIdTestCase(unittest.TestCase):
    @patch('core.similarity.corpus.hal.HAL.create_word_to_word_matrix', MagicMock())
    def test(self):
        expected_term_id = 0

        Document.set_tokenizer(CodeTokenizer())
        documents = []
        documents.append(Document(1, "test", "", ""))
        texts = []

        for doc in documents:
            texts.append(" ".join(doc.get_stemmed_tokens()))
        # HAL.create_word_to_word_matrix = MagicMock()
        h = HAL(texts)
        self.assertEqual(h.get_term_id("test"), expected_term_id)

class HALSearchTestCase(unittest.TestCase):

    # @patch('core.similarity.corpus.hal.HAL.create_word_to_word_matrix', MagicMock())
    def test(self):


        Document.set_tokenizer(CodeTokenizer())
        documents = []
        documents.append(Document(1, "test", "", ""))
        documents.append(Document(2, "document", "", ""))
        texts = []
        expected_doc_id = 1

        for doc in documents:
            texts.append(" ".join(doc.get_stemmed_tokens()))
        # HAL.create_word_to_word_matrix = MagicMock()
        h = HAL(texts)
        new_document = Document(3, "document", "", "")
        results = h.search(new_document.get_stemmed_tokens())

        self.assertEqual(results[0][0], expected_doc_id)