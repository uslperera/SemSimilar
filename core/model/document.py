from nltk.tokenize.api import TokenizerI
from core.textprocessor.wsd import get_synsets
from core.textprocessor.processor import *
import logging

class Document(object):
    """
    Document class includes the basic skeleton to keep all the data associated with posts or articles.
    """
    __id = None
    __title = None
    __description = None
    __tags = None
    __tokens = None
    __synsets = None
    __stemmed_tokens = None
    __tokenizer = None
    __window = 4
    title_enabled = True
    description_enabled = tags_enabled = False
    __synset_tokens = None

    __logger = None

    def __init__(self, id, title, description, tags):
        self.__logger = logging.getLogger(__name__)
        self.__logger.info("Started creating document with id %s", id)

        self.__id = id
        self.__title = title
        self.__description = description
        self.__tags = tags
        self.generate_tokens()
        self.__logger.info("Finished creating document with id %s", id)

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, id):
        self.__id = id

    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, title):
        self.__title = title

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, description):
        self.__description = description

    @property
    def tags(self):
        return self.__tags

    @tags.setter
    def tags(self, tags):
        self.__tags = tags

    @property
    def synset_tokens(self):
        return self.__synset_tokens

    @property
    def stemmed_tokens(self):
        """Return stemmed tokens in the document"""
        return self.__stemmed_tokens

    @property
    def tokens(self):
        return self.__tokens

    @property
    def synsets(self):
        return self.__synsets

    @staticmethod
    def set_window(window):
        """
        Set the size of the window to be used for word sense disambiguation
        min value - 2 & even number
        """
        if window > 1 & window % 2 == 0:
            Document.__window = window

    @staticmethod
    def set_tokenizer(tokenizer):
        """
        Possible tokenizers - semsimilar.core.textprocessor.tokenize.CodeTokenizer, nltk.tokenize.api.*
        """
        if isinstance(tokenizer, TokenizerI):
            Document.__tokenizer = tokenizer

    def generate_tokens(self):
        """Tokenize the document"""
        self.__logger.info("NLP processing started")
        self.__tokens = []
        if self.title_enabled & self.description_enabled & self.tags_enabled:
            text = self.__title + " " + self.__description + " " + self.__tags
            self.__synset_tokens = self.__tokenizer.tokenize((self.__title + " " + self.__tags).lower())
        elif self.title_enabled & self.description_enabled:
            text = self.__title + " " + self.__description
            self.__synset_tokens = self.__tokenizer.tokenize(self.__title.lower())
        elif self.title_enabled & self.tags_enabled:
            text = self.__title + " " + self.__tags
            self.__synset_tokens = self.__tokenizer.tokenize((self.__title + " " + self.__tags).lower())
        else:
            text = self.__title
            self.__synset_tokens = self.__tokenizer.tokenize(self.__title.lower())

        tokens = self.__tokenizer.tokenize(text.lower())
        self.__logger.debug("Tokens %s", tokens)
        self.__tokens = remove_stopwords(tokens)
        self.__logger.debug("Tokens after stop words are removed %s", self.__tokens)

        self.__synset_tokens = remove_stopwords(self.__synset_tokens)
        self.__logger.debug("Synset tokens %s", self.__synset_tokens)
        self.__synsets = get_synsets(self.__synset_tokens, self.__window)
        self.__logger.debug("Synsets %s", self.__synsets)
        self.__stemmed_tokens = stem_tokens(self.__tokens)
        self.__logger.debug("Stemmed tokens %s", self.__stemmed_tokens)
        self.__logger.info("Finished processing the document")