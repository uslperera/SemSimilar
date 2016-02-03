from core.textprocessor import Processor


class DocumentsBuilder(object):
    title_enabled = True
    description_enabled = False
    tags_enabled = False

    __processor = Processor()
    __documents = None

    def __init__(self, documents):
        self.__documents = documents

    def process(self):
        for document in self.__documents:
            if self.title_enabled & self.description_enabled & self.tags_enabled:
                text = document.title + " " + document.description + " " + document.tags
            elif self.title_enabled & self.description_enabled:
                text = document.title + " " + document.description
            elif self.title_enabled & self.tags_enabled:
                text = document.title + " " + document.tags
            else:
                text = document.title

            tokens = self.__processor.process(text)
            document.tokens = tokens
