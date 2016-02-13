import re


def tokenize(text):
    expression = "([?!:;\-\(\)\[\]\"/,<>]|(\.\B))"
    text = re.sub(expression, " ", text).strip()
    tokens = re.split("\s+", text)
    return tokens
