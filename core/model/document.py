from nltk.tokenize.api import TokenizerI
from core.textprocessor.synsets import get_synsets
from core.textprocessor.processor import *


class Document(object):
    __id = None
    __title = None
    __description = None
    __tags = None
    __tokens = None
    __synsets = None
    __tokenizer = None
    __window = 4
    title_enabled = description_enabled = tags_enabled = False

    def __init__(self, id, title, description, tags):
        self.__id = id
        self.__title = title
        self.__description = description
        self.__tags = tags
        self.generate_tokens()
        self.__synsets = get_synsets(self.__tokens, self.__window)

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
    def tokens(self):
        return self.__tokens

    @tokens.setter
    def tokens(self, tokens):
        self.__tokens = tokens

    @property
    def synsets(self):
        return self.__synsets

    @synsets.setter
    def synsets(self, synsets):
        self.__synsets = synsets

    @staticmethod
    def window(window):
        if window > 1 & window % 2 == 0:
            Document.__window = window

    @staticmethod
    def tokenizer(tokenizer):
        if isinstance(tokenizer, TokenizerI):
            Document.__tokenizer = tokenizer

    def generate_tokens(self):
        if self.title_enabled & self.description_enabled & self.tags_enabled:
            text = self.__title + " " + self.__description + " " + self.__tags
        elif self.title_enabled & self.description_enabled:
            text = self.__title + " " + self.__description
        elif self.title_enabled & self.tags_enabled:
            text = self.__title + " " + self.__tags
        else:
            text = self.__title
        tokens = self.__tokenizer.tokenize(text.lower())
        tokens = remove_stopwords(tokens)
        # tokens = stem_tokens(tokens)
        self.__tokens = tokens
