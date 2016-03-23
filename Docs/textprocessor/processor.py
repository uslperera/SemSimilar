# from nltk.stem.porter import PorterStemmer
# from nltk.stem.snowball import SnowballStemmer
# from nltk.corpus import stopwords

# en_stop = stopwords.words('english')
# p_stemmer = PorterStemmer()
# s_stemmer = SnowballStemmer("english")

en_stop= []

def remove_stopwords(tokens):
    """Remove stop words in English

    :param tokens: list of words
    :type tokens: list<string>
    :returns: list of words
    :rtype: list<string>

    :Example:

    >>> tokens = ['this', 'is', 'a', 'demo']
    >>> remove_stopwords(tokens)
    """
    stopped_tokens = [i for i in tokens if not i in en_stop]
    return stopped_tokens


def stem_tokens(tokens):
    """Extract the stem of tokens

    :param tokens: list of words
    :type tokens: list<string>
    :returns: list of words
    :rtype: list<string>

    :Example:

    >>> tokens = ['this', 'is', 'a', 'demo']
    >>> stem_tokens(tokens)
    """
    stemmed_tokens = [i for i in tokens]
    return stemmed_tokens


def remove_custom_words(custom_words, tokens):
    """Remove custom list of words

    :param custom_words: list of words to be removed
    :param tokens: list of words
    :type custom_words: list<string>
    :type tokens: list<string>
    :returns: list of words
    :rtype: list<string>

    :Example:

    >>> tokens = ['this', 'is', 'a', 'demo']
    >>> remove_custom_words(['is'], tokens)
    """
    return
