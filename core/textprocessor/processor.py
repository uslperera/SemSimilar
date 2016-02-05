from nltk.stem.porter import PorterStemmer
from stop_words import get_stop_words
from core.textprocessor import tokenizer

en_stop = get_stop_words('en')
p_stemmer = PorterStemmer()


def remove_stopwords(tokens):
    stopped_tokens = [i for i in tokens if not i in en_stop]
    return stopped_tokens


def stem_tokens(tokens):
    stemmed_tokens = [p_stemmer.stem(i) for i in tokens]
    return stemmed_tokens


def process(text):
    tokens = tokenizer.tokenize(text.lower())
    tokens = remove_stopwords(tokens)
    # tokens = self.stem_tokens(tokens)
    return tokens
