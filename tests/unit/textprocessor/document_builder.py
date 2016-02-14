import unittest
from mock.mock import MagicMock
from core.textprocessor import processor
from core.textprocessor import document_builder
from core.model.document import Document
from nltk import wsd


class DocumentBuildTestCase(unittest.TestCase):
    def test_title_process(self):
        tokens = ["home", "owner"]
        documents = [Document(id=1, title="Test title1", description="", tags=""),
                     Document(id=1, title="Test title2", description="", tags="")]
        processor.process = MagicMock(return_value=tokens)
        # document_builder.generate_window = MagicMock(return_value=tokens)
        wsd.lesk = MagicMock(return_value=None)
        document_builder.process(documents, True, False, False, 0)
        self.assertEqual(len(documents[0].synsets), 2)

    def test_title_tags_process(self):
        tokens = ["home", "owner"]
        documents = [Document(id=1, title="Test title1", description="", tags=""),
                     Document(id=1, title="Test title2", description="", tags="")]
        processor.process = MagicMock(return_value=tokens)
        # document_builder.generate_window = MagicMock(return_value=tokens)
        wsd.lesk = MagicMock(return_value=None)
        document_builder.process(documents, True, False, True, 0)
        self.assertEqual(len(documents[0].synsets), 2)

    def test_title_descriptions_process(self):
        tokens = ["home", "owner"]
        documents = [Document(id=1, title="Test title1", description="", tags=""),
                     Document(id=1, title="Test title2", description="", tags="")]
        processor.process = MagicMock(return_value=tokens)
        # document_builder.generate_window = MagicMock(return_value=tokens)
        wsd.lesk = MagicMock(return_value=None)
        document_builder.process(documents, True, False, True, 0)
        self.assertEqual(len(documents[0].synsets), 2)

    def test_title_description_tags_process(self):
        tokens = ["home", "owner"]
        documents = [Document(id=1, title="Test title1", description="", tags=""),
                     Document(id=1, title="Test title2", description="", tags="")]
        processor.process = MagicMock(return_value=tokens)
        # document_builder.generate_window = MagicMock(return_value=tokens)
        wsd.lesk = MagicMock(return_value=None)
        document_builder.process(documents, True, True, True, 0)
        self.assertEqual(len(documents[0].synsets), 2)

    def test_valid_window(self):
        # A window is valid if its size is greater than 1 and divisible by 2
        expected_window = 4
        window = document_builder.validate_window(expected_window)
        self.assertEqual(window, expected_window)

    def test_invalid_window(self):
        expected_window = 4
        window = document_builder.validate_window(1)
        self.assertEqual(window, expected_window)

    def test_short_text(self):
        tokens = ["home", "owner", "garage"]
        sentence = document_builder.generate_window(4, tokens, 'owner')
        self.assertEqual(str(sentence), str(tokens))

    def test_token_at_the_begining(self):
        tokens = ["home", "owner", "garage", "car", "new"]
        sentence = document_builder.generate_window(2, tokens, "home")
        self.assertEqual(str(sentence), str(["home", "owner", "garage"]))

    def test_token_in_the_middle(self):
        tokens = ["home", "owner", "garage", "car", "new"]
        sentence = document_builder.generate_window(2, tokens, "owner")
        self.assertEqual(str(sentence), str(["home", "owner", "garage"]))

    def test_token_in_the_end(self):
        tokens = ["home", "owner", "garage", "car", "new"]
        sentence = document_builder.generate_window(2, tokens, "new")
        self.assertEqual(str(sentence), str(["garage", "car", "new"]))
