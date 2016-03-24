import unittest

from core.textprocessor.tokenize import CodeTokenizer


class TokenizeSplitTestCase(unittest.TestCase):
    def test(self):
        """Checks whether important symbols are getting removed E.g. # +"""
        expected_tokens = ['tool', 'for', 'converting', 'visual', 'j#', 'code', 'to', 'c++']
        sentence = "Tool for Converting Visual J# code to C++"
        tokens = CodeTokenizer().tokenize(sentence)
        self.assertEqual(str(expected_tokens), str(tokens))


class TokenizePunctuationsTestCase(unittest.TestCase):
    def test(self):
        """Checks whether punctuation marks are getting removed"""
        expected_tokens = ['word']
        sentence = "?!:;-()[]\"/,<>word"
        tokens = CodeTokenizer().tokenize(sentence)
        self.assertEqual(str(expected_tokens), str(tokens))


class TokenizeDotTestCase(unittest.TestCase):
    def test(self):
        """Checks for the behaviour when there is a dot before and after a word"""
        expected_tokens = ['this', 'is', 'a', '.net', 'test']
        sentence = "This is a .NET test."
        tokens = CodeTokenizer().tokenize(sentence)
        self.assertEqual(str(expected_tokens), str(tokens))


class TokenizeWhitespaceTestCase(unittest.TestCase):
    def test(self):
        """Checks for the behaviour when there is a dot before and after a word"""
        expected_tokens = ['this', 'is', 'a', 'whitespace', 'test']
        sentence = "   This is a whitespace       test.   "
        tokens = CodeTokenizer().tokenize(sentence)
        self.assertEqual(str(expected_tokens), str(tokens))


class TokenizeMixTestCase(unittest.TestCase):
    def test(self):
        """Checks for the behaviour when there is a dot before and after a word"""
        expected_tokens = ['i', 'said', 'what', 'are', 'you', 'crazy', 'said', 'sandowsky', 'i', 'cannot', 'afford',
                           'to', 'do', 'that']
        sentence = "\"I said, 'what're you? Crazy?\" said Sandowsky. \"I can't afford to do that.\""
        tokens = CodeTokenizer().tokenize(sentence)
        self.assertEqual(str(expected_tokens), str(tokens))

class TokenizeSpanTokenizeTestCase(unittest.TestCase):
    def test(self):
        sentence = "This is a test."
        CodeTokenizer().span_tokenize(sentence)