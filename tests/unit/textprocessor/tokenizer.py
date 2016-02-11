import unittest
from core.textprocessor.tokenizer import tokenize


class TokenizeTestCase(unittest.TestCase):
    '''Tests for tokenizer'''

    def test_split(self):
        # Checks whether important symbols are getting removed E.g. # +
        expected_tokens = ['Tool', 'for', 'Converting', 'Visual', 'J#', 'code', 'to', 'C++']
        sentence = "Tool for Converting Visual J# code to C++"
        tokens = tokenize(sentence)
        self.assertEqual(str(expected_tokens), str(tokens))

    def test_punctuations(self):
        # Checks whether punctuation marks are getting removed
        expected_tokens = ['word']
        sentence = "?!:;-()[]\"/,<>word"
        tokens = tokenize(sentence)
        self.assertEqual(str(expected_tokens), str(tokens))

    def test_dot(self):
        # Checks for the behaviour when there is a dot before and after a word
        expected_tokens = ['This', 'is', 'a', '.NET', 'test']
        sentence = "This is a .NET test."
        tokens = tokenize(sentence)
        self.assertEqual(str(expected_tokens), str(tokens))

    def test_whitespace(self):
        # Checks for the behaviour when there is a dot before and after a word
        expected_tokens = ['This', 'is', 'a', 'whitespace', 'test']
        sentence = "   This is a whitespace       test.   "
        tokens = tokenize(sentence)
        self.assertEqual(str(expected_tokens), str(tokens))

    def test_mix(self):
        # Checks for the behaviour when there is a dot before and after a word
        expected_tokens = ['I', 'said', 'what', 're', 'you', 'Crazy', 'said', 'Sandowsky', 'I', 'can', 't', 'afford',
                           'to', 'do', 'that']
        sentence = "\"I said, 'what're you? Crazy?\" said Sandowsky. \"I can't afford to do that.\""
        tokens = tokenize(sentence)
        self.assertEqual(str(expected_tokens), str(tokens))


if __name__ == '__main__':
    unittest.main()
