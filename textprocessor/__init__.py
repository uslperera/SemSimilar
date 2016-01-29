import re
from nltk.stem.porter import PorterStemmer
from stop_words import get_stop_words


class SemSimilarTokenizer(object):
    @staticmethod
    def tokenize(text):
        expression = "([?!:;\-\(\)\[\]'\"/,]|(\.\B))"
        text = re.sub(expression, " ", text).strip()
        tokens = re.split("\s+", text)
        return tokens


class Processor(object):
    __en_stop = get_stop_words('en')
    __p_stemmer = PorterStemmer()

    @staticmethod
    def tokenize(text):
        return SemSimilarTokenizer.tokenize(text)

    def remove_stopwords(self, tokens):
        stopped_tokens = [i for i in tokens if not i in self.__en_stop]
        return stopped_tokens

    def stem_tokens(self, tokens):
        stemmed_tokens = [self.__p_stemmer.stem(i) for i in tokens]
        return stemmed_tokens

    def process(self, text):
        tokens = SemSimilarTokenizer.tokenize(text.lower())
        tokens = self.remove_stopwords(tokens)
        return tokens


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
