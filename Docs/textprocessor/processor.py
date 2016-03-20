# from nltk.stem.porter import PorterStemmer
# from nltk.stem.snowball import SnowballStemmer
# from nltk.corpus import stopwords

# en_stop = stopwords.words('english')
# p_stemmer = PorterStemmer()
# s_stemmer = SnowballStemmer("english")

en_stop= []

def remove_stopwords(tokens):
    """
    Remove stop words in English (e.g. and, of, for, to)

    Refer for the full list:
    http://www.ranks.nl/stopwords
    """
    stopped_tokens = [i for i in tokens if not i in en_stop]
    return stopped_tokens


def stem_tokens(tokens):
    """Extract the stem of words"""
    stemmed_tokens = [i for i in tokens]
    return stemmed_tokens


# def remove_meta_data(tokens):
#     keywords = ['blockquote', '&#xa', 'p', 'strong', '\\', 'br', 'a', 'code', 'pre']
#     filtered_tokens = [i for i in tokens if not i in keywords]
#     return filtered_tokens
