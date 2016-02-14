import re


def tokenize(text):
    expression = "([?!:;\-\(\)\[\]\"/,<>]|(\.\B)|(\s'))"
    text = re.sub(expression, " ", text).strip()
    tokens = re.split("\s+", text)
    return tokens
