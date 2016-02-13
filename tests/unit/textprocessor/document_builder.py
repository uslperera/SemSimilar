import unittest
from core.textprocessor.document_builder import *
from core.model.document import Document


class DocumentBuildTestCase(unittest.TestCase):
    def test_title_process(self):
        documents = [Document(id=1, title="Test title1", description="", tags=""),
                     Document(id=1, title="Test title2", description="", tags="")]
