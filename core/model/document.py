class Document(object):
    __id = None
    __title = None
    __description = None
    __tags = None
    __tokens = None

    def __init__(self, id, title, description, tags):
        self.__id = id
        self.__title = title
        self.__description = description
        self.__tags = tags

    @property
    def id(self):
        return self.__id

    @id.setter
    def title(self, id):
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
