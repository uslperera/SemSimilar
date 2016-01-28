import re
from nltk.stem.porter import PorterStemmer
from stop_words import get_stop_words


class SemSimilarTokenizer(object):
    def tokenize(self, text):
        text = re.sub("([?!:;\-\(\)\[\]'\"/,]|(\.\B))", " ", text).strip()
        tokens = re.split("\s+", text)
        return tokens


class Processor(object):
    __en_stop = get_stop_words('en')
    __p_stemmer = PorterStemmer()

    def tokenize(self, text):
        return SemSimilarTokenizer().tokenize(text.lower())

    def remove_stopwords(self, tokens):
        stopped_tokens = [i for i in tokens if not i in self.__en_stop]
        return stopped_tokens

    def stem_tokens(self, tokens):
        stemmed_tokens = [self.__p_stemmer.stem(i) for i in tokens]
        return stemmed_tokens

    def process(self, text):
        tokens = self.tokenize(text)
        tokens = self.remove_stopwords(tokens)
        return self.stem_tokens(tokens)
