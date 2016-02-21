import unittest
from core.model.document import Document
from core.tokenize import CodeTokenizer


class WindowTestCase(unittest.TestCase):
    def test_set_window(self):
        Document.window(6)


class TokenizerTestCase(unittest.TestCase):
    def test_set_tokenizer(self):
        Document.tokenizer(CodeTokenizer())


class IDTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        Document.tokenizer(CodeTokenizer())

    def test_set_id(self):
        d = Document(0, "", "", "")
        d.id = 1
        self.assertEqual(d.id, 1)

    def test_get_id(self):
        d = Document(1, "", "", "")
        self.assertEqual(d.id, 1)


class TitleTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        Document.tokenizer(CodeTokenizer())

    def test_set_title(self):
        d = Document(0, "", "", "")
        d.title = "A"
        self.assertEqual(d.title, "A")

    def test_get_title(self):
        d = Document(0, "A", "", "")
        self.assertEqual(d.title, "A")


class DescriptionTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        Document.tokenizer(CodeTokenizer())

    def test_set_description(self):
        d = Document(0, "", "", "")
        d.description = "A"
        self.assertEqual(d.description, "A")

    def test_get_description(self):
        d = Document(0, "", "A", "")
        self.assertEqual(d.description, "A")


class TagsTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        Document.tokenizer(CodeTokenizer())

    def test_set_tags(self):
        d = Document(0, "", "", "")
        d.tags = "A"
        self.assertEqual(d.tags, "A")

    def test_get_tags(self):
        d = Document(0, "", "", "A")
        self.assertEqual(d.tags, "A")


class TokensOptionTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        Document.tokenizer(CodeTokenizer())

    def setUp(self):
        Document.title_enabled = Document.description_enabled = Document.tags_enabled = False

    def test_all_options(self):
        expected_tokens = ["title", "description", "tags"]
        Document.title_enabled = Document.description_enabled = Document.tags_enabled = True
        d = Document(1, "title", "description", "tags")
        self.assertEqual(str(d.tokens), str(expected_tokens))

    def test_title_description(self):
        expected_tokens = ["title", "description"]
        Document.title_enabled = Document.description_enabled = True
        d = Document(1, "title", "description", "tags")
        self.assertEqual(str(d.tokens), str(expected_tokens))

    def test_title_tags(self):
        expected_tokens = ["title", "tags"]
        Document.title_enabled = Document.tags_enabled = True
        d = Document(1, "title", "description", "tags")
        self.assertEqual(str(d.tokens), str(expected_tokens))

    def test_title(self):
        expected_tokens = ["title"]
        d = Document(1, "title", "description", "tags")
        self.assertEqual(str(d.tokens), str(expected_tokens))
