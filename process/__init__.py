import re

class SpecialTokenizer(object):

    def tokenize(self, text):
        text = re.sub("[?\.!:;\-\(\)\[\]'\"/,]", " ", text)
        tokens = re.split("\s+", text)
        return tokens
