from nltk.stem.porter import PorterStemmer
from stop_words import get_stop_words
from core.textprocessor import SemSimilarTokenizer


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
        # tokens = self.stem_tokens(tokens)
        return tokens
