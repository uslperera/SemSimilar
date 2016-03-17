import unittest
from mock.mock import MagicMock, patch
from core.textprocessor import wsd


class SynsetTestCase(unittest.TestCase):
    @patch('core.textprocessor.wsd.generate_window',
           MagicMock(return_value=["home", "owner", "garage", "car"]))
    def test_synsets_without_none(self):
        expected_synset = [u'home.v.02', u'owner.n.02', u'garage.v.01', u'car.n.04']
        tokens = ["home", "owner", "garage", "car"]
        s = wsd.get_synsets(tokens, 4)

        self.assertEqual(str(s), str(expected_synset))


class WindowTestCase(unittest.TestCase):
    def test_valid_window(self):
        # A set_window is valid if its size is greater than 1 and divisible by 2
        expected_window = 4
        window = wsd.validate_window(expected_window)
        self.assertEqual(window, expected_window)

    def test_invalid_window(self):
        expected_window = 4
        window = wsd.validate_window(1)
        self.assertEqual(window, expected_window)


class GenerateSentenceTestCase(unittest.TestCase):
    def test_short_text(self):
        tokens = ["home", "owner", "garage"]
        sentence = wsd.generate_window(4, tokens, 'owner')
        self.assertEqual(str(sentence), str(tokens))

    def test_token_at_the_begining(self):
        tokens = ["home", "owner", "garage", "car", "new"]
        sentence = wsd.generate_window(2, tokens, "home")
        self.assertEqual(str(sentence), str(["home", "owner", "garage"]))

    def test_token_in_the_middle(self):
        tokens = ["home", "owner", "garage", "car", "new"]
        sentence = wsd.generate_window(2, tokens, "owner")
        self.assertEqual(str(sentence), str(["home", "owner", "garage"]))

    def test_token_in_the_end(self):
        tokens = ["home", "owner", "garage", "car", "new"]
        sentence = wsd.generate_window(2, tokens, "new")
        self.assertEqual(str(sentence), str(["garage", "car", "new"]))
