import unittest
from mock.mock import patch

from semsimilar.similarity_core.main import ss_similarity
from semsimilar.model.document import Document
from semsimilar.textprocessor.tokenize import CodeTokenizer
from semsimilar.similarity_core.corpus.hal import HAL

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
            texts.append(" ".join(document.stemmed_tokens))

        # generate HAL model
        # Topics are health, food, motor
        cls.hal = HAL(texts)

    @patch('semsimilar.similarity_core.knowledge.lesk.similarity')
    @patch('semsimilar.similarity_core.corpus.hal.HAL.semantic_search')
    def test_similarity(self, hal, lesk):
        """Check for similarity_core"""
        expected_document = self.documents[0]
        expected_score = 1.0

        hal.return_value = [(1, 0.989899), (0, 0.70009)]
        lesk.return_value = [(self.documents[0], 1.0), (self.documents[1], 0.890909)]

        new_document = Document(0, "Brocolli is a good vegetable for health", "", "Health, Food")
        results = ss_similarity(self.documents, new_document, self.hal, 1)
        top_doc, score = results[0]

        self.assertEqual(top_doc.id, expected_document.id)
        self.assertEqual(score, expected_score)
