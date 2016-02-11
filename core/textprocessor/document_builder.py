from core.textprocessor import processor
from nltk.wsd import lesk


def process(documents, title_enabled, description_enabled, tags_enabled, window):
    window = __validate_window(window)
    for document in documents:
        if title_enabled & description_enabled & tags_enabled:
            text = document.title + " " + document.description + " " + document.tags
        elif title_enabled & description_enabled:
            text = document.title + " " + document.description
        elif title_enabled & tags_enabled:
            text = document.title + " " + document.tags
        else:
            text = document.title

        tokens = processor.process(text)
        document.tokens = tokens
        synsets = []
        for token in tokens:
            sentence = __generate_window(window, tokens, token)
            synset = lesk(sentence, token)
            if synset is not None:
                synsets.append(synset.name())
            else:
                synsets.append(None)
        document.synsets = synsets


def __generate_window(window, tokens, target):
    new_tokens = []
    index = tokens.index(target)
    right = 0
    if len(tokens) < window + 1:
        return " ".join(tokens)
    # if index of the target word is greater than or equal to half of the windows size
    if index >= (window / 2):
        left = index - (window / 2)
    else:
        left = 0
        right = (window / 2) - index
    # if index of the target
    if (index + right + (window / 2)) < len(tokens):
        right = index + right + (window / 2) + 1
    else:
        right = len(tokens)
        left -= (index + (window / 2) + 1) - len(tokens)
    for num in range(left, right):
        new_tokens.append(tokens[num])

    return new_tokens


def __validate_window(window):
    default_window = 4
    if window > 1 & window % 2 == 0:
        return window
    else:
        return default_window
