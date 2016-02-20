from nltk.stem.porter import PorterStemmer
from nltk.stem.snowball import SnowballStemmer
from stop_words import get_stop_words

en_stop = get_stop_words('en')
p_stemmer = PorterStemmer()
s_stemmer = SnowballStemmer("english")


def remove_stopwords(tokens):
    stopped_tokens = [i for i in tokens if not i in en_stop]
    return stopped_tokens


def stem_tokens(tokens):
    stemmed_tokens = [s_stemmer.stem(i) for i in tokens]
    return stemmed_tokens


def remove_meta_data(tokens):
    keywords = ['blockquote', '&#xa', 'p', 'strong', '\\', 'br', 'a', 'code', 'pre']
    filtered_tokens = [i for i in tokens if not i in keywords]
    return filtered_tokens
