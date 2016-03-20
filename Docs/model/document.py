# from nltk.tokenize.api import TokenizerI
# from core.textprocessor.wsd import get_synsets
# from core.textprocessor.processor import *


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

    def __init__(self, id, title, description, tags):
        """
        Create a new document
        Document(1, "Title", "Description", "Tags")
        """
        self.__id = id
        self.__title = title
        self.__description = description
        self.__tags = tags
        self.generate_tokens()

    @property
    def id(self):
        """Get id of the document"""
        return self.__id

    @id.setter
    def id(self, id):
        """Set id of the document"""
        self.__id = id

    @property
    def title(self):
        """Get title of the document"""
        return self.__title

    @title.setter
    def title(self, title):
        """Set title of the document"""
        self.__title = title

    @property
    def description(self):
        """Get description of the document"""
        return self.__description

    @description.setter
    def description(self, description):
        """Set description of the document"""
        self.__description = description

    @property
    def tags(self):
        """Get tags of the document"""
        return self.__tags

    @tags.setter
    def tags(self, tags):
        """Set tags of the document"""
        self.__tags = tags

    @property
    def synset_tokens(self):
        """Get synsets of the tokens (Description is excluded)"""
        return self.__synset_tokens

    @property
    def stemmed_tokens(self):
        """Get stemmed tokens of the document"""
        return self.__stemmed_tokens

    @property
    def tokens(self):
        """Get tokens of the document"""
        return self.__tokens

    @property
    def synsets(self):
        """Get synsets of the tokens (Description is included)"""
        return self.__synsets

    @staticmethod
    def set_window(window):
        """
        Set the size of the window to be used for word sense disambiguation

        min value = 2 & must be even number
        """
        if window > 1 & window % 2 == 0:
            Document.__window = window

    @staticmethod
    def set_tokenizer(tokenizer):
        """
        Set a tokenizer to extract words

        Possible tokenizers - semsimilar.core.textprocessor.tokenize.CodeTokenizer, nltk.tokenize.api.*
        """
        return

    def generate_tokens(self):
        """Tokenize the document based on selected components (title | description | tags)"""
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
        # tokens = remove_stopwords(tokens)
        self.__tokens = tokens

        self.__synset_tokens = remove_stopwords(self.__synset_tokens)
        # self.__synsets = get_synsets(self.__tokens, self.__window)
        # self.__synsets = get_synsets(self.__synset_tokens, self.__window)
        self.__stemmed_tokens = stem_tokens(self.__tokens)
