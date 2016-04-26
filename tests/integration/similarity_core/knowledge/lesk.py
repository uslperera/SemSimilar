import unittest
from semsimilar.model.document import Document
from semsimilar.similarity_core.knowledge import lesk as lesk
from semsimilar.textprocessor.tokenize import CodeTokenizer


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

    def test_invalid_count(self):
        """If an invalid count is given"""
        expected_count = 1

        new_document = Document(0, "Brocolli is a good vegetable for health", "", "Health, Food")
        results = lesk.similarity(self.documents, new_document, 0)

        self.assertEqual(len(results), expected_count)

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

    def test_semantic_score(self):
        """Check if the similarity score is calculated correctly"""
        individual_score = 1
        """Calculate the semantic relatedness score"""

        new_document = Document(0, "Brocolli is a good vegetable for health", "", "Health, Food")
        expected_score = (((len(self.documents[1].tokens) - 1) * individual_score + 1) + (len(
                new_document.tokens) - 1) * individual_score + 1) / (
                             len(self.documents[1].tokens) + len(new_document.tokens))
        # subtracted 1 to consider None in synsets
        results = lesk.similarity(self.documents, new_document, 1)
        top_doc, score = results[0]

        self.assertEqual(round(score, 2), round(expected_score, 2))
