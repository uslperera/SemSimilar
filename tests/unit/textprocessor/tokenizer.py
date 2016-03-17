import unittest

from core.textprocessor.tokenize import CodeTokenizer


class TokenizeSplitTestCase(unittest.TestCase):
    def test(self):
        """Checks whether important symbols are getting removed E.g. # +"""
        expected_tokens = ['Tool', 'for', 'Converting', 'Visual', 'J#', 'code', 'to', 'C++']
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
        expected_tokens = ['This', 'is', 'a', '.NET', 'test']
        sentence = "This is a .NET test."
        tokens = CodeTokenizer().tokenize(sentence)
        self.assertEqual(str(expected_tokens), str(tokens))


class TokenizeWhitespaceTestCase(unittest.TestCase):
    def test(self):
        """Checks for the behaviour when there is a dot before and after a word"""
        expected_tokens = ['This', 'is', 'a', 'whitespace', 'test']
        sentence = "   This is a whitespace       test.   "
        tokens = CodeTokenizer().tokenize(sentence)
        self.assertEqual(str(expected_tokens), str(tokens))


class TokenizeMixTestCase(unittest.TestCase):
    def test(self):
        """Checks for the behaviour when there is a dot before and after a word"""
        expected_tokens = ['I', 'said', 'what\'re', 'you', 'Crazy', 'said', 'Sandowsky', 'I', 'can\'t', 'afford',
                           'to', 'do', 'that']
        sentence = "\"I said, 'what're you? Crazy?\" said Sandowsky. \"I can't afford to do that.\""
        tokens = CodeTokenizer().tokenize(sentence)
        self.assertEqual(str(expected_tokens), str(tokens))

class TokenizeSpanTokenizeTestCase(unittest.TestCase):
    def test(self):
        sentence = "This is a test."
        CodeTokenizer().span_tokenize(sentence)