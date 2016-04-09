import unittest
from semsimilar.model.document import Document
from semsimilar.textprocessor.tokenize import CodeTokenizer
from semsimilar.similarity.corpus.hal import HAL
from semsimilar.similarity.knowledge import lesk
from semsimilar.similarity.main import ss_similarity

Document.set_tokenizer(CodeTokenizer())


class TokenizerTestCase(unittest.TestCase):
    def test(self):
        Document.description_enabled = False
        d = Document(0, "\"I said, 'what're you? Crazy?\" said Sandowsky. \"I can't afford to do that.\"", None, None)
        expected_tokens = ['said', 'crazy', 'said', 'sandowsky', 'cannot', 'afford']
        self.assertEqual(str(d.tokens), str(expected_tokens))


class StopWordRemovalTestCase(unittest.TestCase):
    def test(self):
        Document.description_enabled = False
        d = Document(0, "This is a sample text to test stop word removal", None, None)
        expected_tokens = ['sample', 'text', 'test', 'stop', 'word', 'removal']
        self.assertEqual(str(d.tokens), str(expected_tokens))


class SpecialWordRemovalTestCase(unittest.TestCase):
    def test(self):
        Document.description_enabled = False
        d = Document(0, "This is a sample text to test special word removal", None, None)
        expected_tokens = ['sample', 'text', 'test', 'removal']
        d.remove_special_words(['special', 'word'])
        self.assertEqual(str(d.tokens), str(expected_tokens))


class StemWordsDocumentTestCase(unittest.TestCase):
    def test(self):
        Document.description_enabled = False
        d = Document(0, "Walking walks walked", None, None)
        expected_tokens = [u'walk', u'walk', u'walk']
        self.assertEqual(str(d.stemmed_tokens), str(expected_tokens))


class HALSearchTestCase(unittest.TestCase):
    def test1(self):
        Document.description_enabled = False
        doc_a = Document(1, "Some health experts suggest that driving may cause increased tension and blood pressure.",
                         "",
                         "Health, Motor")
        doc_b = Document(2, "Health professionals say that brocolli is good for your health.", "", "Health, Food")
        doc_c = Document(3, "NASA announced plans to send a manned mission to Mars in the 2030.", "", "Science")

        documents = [doc_a, doc_b, doc_c]
        texts = []
        expected_doc_id = 1

        for doc in documents:
            texts.append(" ".join(doc.stemmed_tokens))
        h = HAL(texts)
        new_document = Document(0, "Brocolli is a good vegetable for health", "", "Health, Food")
        results = h.semantic_search(new_document.stemmed_tokens)

        self.assertEqual(results[0][0], expected_doc_id)

    def test2(self):
        Document.description_enabled = False
        doc_a = Document(1, "How do I calculate someone's age in C#", "", "")
        doc_b = Document(2, "Distributed source control options", "", "")

        documents = [doc_a, doc_b]
        texts = []
        expected_doc_id = 1

        for doc in documents:
            texts.append(" ".join(doc.stemmed_tokens))
        h = HAL(texts)
        new_document = Document(0, "calculate age", "", "")
        results = h.semantic_search(new_document.stemmed_tokens)

        self.assertEqual(documents[results[0][0]].id, expected_doc_id)


    def test3(self):
        Document.description_enabled = False
        doc_a = Document(1, "How do I calculate someone's age in C#", "", "")
        doc_b = Document(2, "Distributed source control options", "", "")

        documents = [doc_a, doc_b]
        texts = []
        expected_doc_id = 1

        for doc in documents:
            texts.append(" ".join(doc.stemmed_tokens))
        h = HAL(texts)
        new_document = Document(0, "age in c#", "", "")
        results = h.semantic_search(new_document.stemmed_tokens)

        self.assertEqual(documents[results[0][0]].id, expected_doc_id)

    def test4(self):
        Document.description_enabled = False
        doc_a = Document(1, "How do I calculate someone's age in C#", "", "")
        doc_b = Document(2, "Distributed source control options", "", "")
        doc_c = Document(3, "How do I calculate relative time", "", "")

        documents = [doc_a, doc_b, doc_c]
        texts = []
        expected_doc_id1 = 1
        expected_doc_id2 = 3

        for doc in documents:
            texts.append(" ".join(doc.stemmed_tokens))

        h = HAL(texts)
        new_document = Document(0, "compute age in c#", "", "")
        results = h.semantic_search(new_document.stemmed_tokens)
        self.assertEqual(documents[results[0][0]].id, expected_doc_id1)
        self.assertEqual(documents[results[1][0]].id, expected_doc_id2)


class LeskSearchTestCase(unittest.TestCase):
    def tes1(self):
        Document.description_enabled = False
        doc_a = Document(1, "Some health experts suggest that driving may cause increased tension and blood pressure.",
                         "",
                         "Health, Motor")
        doc_b = Document(2, "Health professionals say that brocolli is good for your health.", "", "Health, Food")
        doc_c = Document(3, "NASA announced plans to send a manned mission to Mars in the 2030.", "", "Science")

        documents = [doc_a, doc_b, doc_c]
        expected_doc_id = 2
        new_document = Document(0, "Brocolli is a good vegetable for health", "", "Health, Food")
        results = lesk.similarity(documents, new_document, 1)

        self.assertEqual(results[0][0].id, expected_doc_id)

    def test2(self):
        Document.description_enabled = False
        doc_a = Document(1, "he tried to break the bank at Monte Carlo", "", "")
        doc_b = Document(2, "he sat on the bank of the river and watched the currents", "", "")

        documents = [doc_a, doc_b]
        expected_doc_id = 1
        new_document = Document(0, "he went to the bank to get a loan", "", "")
        results = lesk.similarity(documents, new_document, 1)

        self.assertEqual(results[0][0].id, expected_doc_id)

    def test3(self):
        Document.description_enabled = False
        doc_a = Document(1, "he tried to break the bank at Monte Carlo", "", "")
        doc_b = Document(2, "he sat on the bank of the river and watched the currents", "", "")

        documents = [doc_a, doc_b]
        expected_doc_id = 1
        new_document = Document(0, "Bank near the river is closed today", "", "")
        results = lesk.similarity(documents, new_document, 1)

        self.assertEqual(results[0][0].id, expected_doc_id)


class MainSearchTestCase(unittest.TestCase):
    def test(self):
        Document.description_enabled = False
        doc_a = Document(1, "Some health experts suggest that driving may cause increased tension and blood pressure.",
                         "",
                         "Health, Motor")
        doc_b = Document(2, "Health professionals say that brocolli is good for your health.", "", "Health, Food")
        doc_c = Document(3, "NASA announced plans to send a manned mission to Mars in the 2030.", "", "Science")

        documents = [doc_a, doc_b, doc_c]
        texts = []
        expected_doc_id = 2

        for doc in documents:
            texts.append(" ".join(doc.stemmed_tokens))

        # generate HAL model
        # Topics are health, food, motor
        hal = HAL(texts)
        new_document = Document(0, "Brocolli is a good vegetable for health", "", "Health, Food")
        results = ss_similarity(documents, new_document, hal, 1)

        self.assertEqual(results[0][0].id, expected_doc_id)


class SelectableComponentsSearchTestCase(unittest.TestCase):
    def test(self):
        Document.description_enabled = True
        doc_a = Document(1, "",
                         "Some health experts suggest that driving may cause increased tension and blood pressure.",
                         "Health, Motor")
        doc_b = Document(2, "", "Health professionals say that brocolli is good for your health.", "Health, Food")
        doc_c = Document(3, "", "NASA announced plans to send a manned mission to Mars in the 2030.", "Science")

        documents = [doc_a, doc_b, doc_c]
        texts = []
        expected_doc_id = 2

        for doc in documents:
            texts.append(" ".join(doc.stemmed_tokens))

        # generate HAL model
        # Topics are health, food, motor
        hal = HAL(texts)
        new_document = Document(0, "Brocolli is a good vegetable for health", "", "Health, Food")
        results = ss_similarity(documents, new_document, hal, 1)

        self.assertEqual(results[0][0].id, expected_doc_id)
