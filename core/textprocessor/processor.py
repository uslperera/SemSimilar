from nltk.stem.porter import PorterStemmer
from nltk.stem.snowball import SnowballStemmer
import stop_words
import logging
en_stop = stop_words.get_stop_words('en')
p_stemmer = PorterStemmer()
s_stemmer = SnowballStemmer("english")


def remove_stopwords(tokens):
    """Remove stop words in English"""
    logger = logging.getLogger(__name__)
    logger.info("Stopwords removal started")
    stopped_tokens = [i for i in tokens if not i in en_stop]
    logger.debug("Stopped tokens %s", stopped_tokens)
    logger.info("Stopwords removal finished")
    return stopped_tokens


def stem_tokens(tokens):
    """Extract the stem of tokens"""
    logger = logging.getLogger(__name__)
    logger.info("Stemming started")
    stemmed_tokens = [s_stemmer.stem(i) for i in tokens]
    logger.debug("Stemmed tokens %s", stemmed_tokens)
    logger.info("Stemming finished")
    return stemmed_tokens


def remove_custom_words(custom_words, tokens):
    logger = logging.getLogger(__name__)
    logger.info("Custom words removal started")
    filtered_tokens = [i for i in tokens if not i in custom_words]
    logger.debug("Tokens after custom words were removed %s", filtered_tokens)
    logger.info("Custom words removal finished")
    return filtered_tokens
