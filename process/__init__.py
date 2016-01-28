import re

class SpecialTokenizer(object):

    def tokenize(self, text):
        text = re.sub("([?!:;\-\(\)\[\]'\"/,]|(\.\B))", " ", text).strip()
        tokens = re.split("\s+", text)
        return tokens