from semsimilar.model.document import Document
from semsimilar.textprocessor.tokenize import CodeTokenizer
import unittest


class TokenizeDocumentTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        Document.set_tokenizer(CodeTokenizer())

    def normal_text_test(self):
        d = Document(0, "This is a sample text", None, None)
        expected_tokens = ['sample', 'text']
        self.assertEqual(str(d.tokens), str(expected_tokens))

    def punctuation_test(self):
        d = Document(0, "?!:;-()[]\"/,<>word", None, None)
        expected_tokens = ['word']
        self.assertEqual(str(d.tokens), str(expected_tokens))

    def dot_test(self):
        d = Document(0, "This is a .NET test.", None, None)
        expected_tokens = ['.net', 'test']
        self.assertEqual(str(d.tokens), str(expected_tokens))

    def whitespace_test(self):
        d = Document(0, "   This is a whitespace       test.   ", None, None)
        expected_tokens = ['whitespace', 'test']
        self.assertEqual(str(d.tokens), str(expected_tokens))

    def mix_text_test(self):
        d = Document(0, "\"I said, 'what're you? Crazy?\" said Sandowsky. \"I can't afford to do that.\"", None, None)
        expected_tokens = ['said', 'crazy', 'said', 'sandowsky', 'afford']
        self.assertEqual(str(d.tokens), str(expected_tokens))

class StopWordRemovalDocumentTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        Document.set_tokenizer(CodeTokenizer())

    def test(self):
        stop_words = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours',
                      'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers',
                      'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves',
                      'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are',
                      'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does',
                      'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until',
                      'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into',
                      'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down',
                      'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here',
                      'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more',
                      'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so',
                      'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now']

        d = Document(0, " ".join(stop_words), None, None)
        self.assertEqual(len(d.tokens), 0)


class StemWordsDocumentTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        Document.set_tokenizer(CodeTokenizer())

    def test(self):
        d = Document(0, "Walking walks walked", None, None)
        expected_tokens = [u'walk', u'walk', u'walk']
        self.assertEqual(str(d.stemmed_tokens), str(expected_tokens))


class SynsetsDocumentTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        Document.set_tokenizer(CodeTokenizer())

    def test(self):
        d = Document(0, "Walking", None, None)
        expected_tokens = [u'walk.v.04']
        self.assertEqual(str(d.synsets), str(expected_tokens))