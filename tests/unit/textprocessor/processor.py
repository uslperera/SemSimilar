import unittest
from semsimilar.textprocessor.processor import *


class StopWordRemovalTestCase(unittest.TestCase):
    def test_remove_stopwords(self):
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
        new_tokens = remove_stopwords(stop_words)
        self.assertEqual(len(new_tokens), 0)


class StemWordsTestCase(unittest.TestCase):
    def test_stem_words(self):
        tokens = ['walked', 'walking', 'walks']
        new_tokens = stem_tokens(tokens)
        for new_token in new_tokens:
            self.assertEqual(new_token, 'walk')

class SpecialWordsTestCase(unittest.TestCase):
    def test(self):
        tokens = ['tool', 'converting', 'visual', 'j#', 'code', 'c++']
        expected_tokens = ['tool', 'converting', 'visual', 'j#', 'c++']
        special_token = ['code']
        new_tokens = remove_custom_words(special_token, tokens)

        self.assertEqual(str(new_tokens), str(expected_tokens))
