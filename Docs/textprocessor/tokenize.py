class CodeTokenizer(object):

    _expression = r"([?!:;\-\(\)\[\]\"/,<>]|(\.\B)|(\s'))"

    def remove_punctuations(self, s):
        """Remove punctuation marks"""
        # return re.sub(self._expression, " ", s).strip()
        return

    def tokenize(self, s):
        """Tokenize a string (Splits the text into words)"""
        # s = self.remove_punctuations(s)
        # return re.split("\s+", s)
        return

    def span_tokenize(self, s):
        pass