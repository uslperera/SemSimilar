import unittest

from mock.mock import MagicMock, patch

from core.model.document import Document
from core.similarity.knowledge import lesk as lesk
from core.textprocessor.tokenize import CodeTokenizer


class OntologyResultCountTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        Document.set_tokenizer(CodeTokenizer())
        doc_a = Document(1, "Some health experts suggest that driving may cause increased tension and blood pressure.",
                         "",
                         "Health, Motor")
        doc_b = Document(2, "Health professionals say that brocolli is good for your health.", "", "Health, Food")
        doc_c = Document(3, "NASA announced plans to send a manned mission to Mars in the 2030.", "", "Science")

        # compile sample documents into a list
        cls.documents = [doc_a, doc_b, doc_c]
        texts = []
        for document in cls.documents:
            texts.append(document.stemmed_tokens)

    @patch('core.model.document.Document.generate_tokens', MagicMock())
    @patch('core.model.document.Document.stemmed_tokens', MagicMock())
    def test_invalid_count(self):
        """If an invalid count is given"""
        expected_count = 1

        new_document = Document(0, "Brocolli is a good vegetable for health", "", "Health, Food")
        results = lesk.similarity(self.documents, new_document, 0)

        self.assertEqual(len(results), expected_count)

    @patch('core.model.document.Document.generate_tokens', MagicMock())
    @patch('core.model.document.Document.stemmed_tokens', MagicMock())
    def test_valid_count(self):
        """If an invalid count is given"""
        expected_count = 2

        new_document = Document(0, "Brocolli is a good vegetable for health", "", "Health, Food")
        results = lesk.similarity(self.documents, new_document, expected_count)

        self.assertEqual(len(results), expected_count)


class SemanticScoreTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        Document.set_tokenizer(CodeTokenizer())
        doc_a = Document(1, "Some health experts suggest that driving may cause increased tension and blood pressure.",
                         "",
                         "Health, Motor")
        doc_b = Document(2, "Brocolli is a good vegetable for health", "", "Health, Food")

        # compile sample documents into a list
        cls.documents = [doc_a, doc_b]
        texts = []
        for document in cls.documents:
            texts.append(document.stemmed_tokens)

    @patch('core.textprocessor.wsd.get_synsets',
           MagicMock(return_value=[None, u'well.r.01', u'vegetable.n.02', u'health.n.02']))
    def test_semantic_score(self):
        """Check if the ss_similarity score is calculated correctly"""
        individual_score = 0.9
        """Calculate the semantic relatedness score"""

        a = MagicMock()
        a.path_similarity.return_value = individual_score

        new_document = Document(0, "Brocolli is a good vegetable for health", "", "Health, Food")
        expected_score = (((len(self.documents[1].tokens) - 1) * individual_score + 1) + (len(
                new_document.tokens) - 1) * individual_score + 1) / (
                             len(self.documents[1].tokens) + len(new_document.tokens))
        # subtracted 1 to consider None in synsets
        with patch('nltk.corpus.wordnet.synset', MagicMock(return_value=a)):
            results = lesk.similarity(self.documents, new_document, 1)
            top_doc, score = results[0]

            self.assertEqual(round(score, 2), round(expected_score, 2))
