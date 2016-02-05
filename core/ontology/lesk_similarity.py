from nltk.wsd import lesk


def similarity(documents, new_document, window, count):
    window = __validate_window(window)
    count = __validate_count(count)

    results = []
    for document in documents:
        score = __get_score(window, new_document, document)
        if len(results) < count:
            result = (document, score)
            results.append(result)
            if len(results) == count:
                results.sort(key=lambda tup: tup[1], reverse=True)
        elif results[count - 1][1] < score:
                results.pop()
                result = (document, score)
                results.append(result)
                results.sort(key=lambda tup: tup[1], reverse=True)
    return results


def __validate_window(window):
    default_window = 4
    if window > 1 & window % 2 == 0:
        return window
    else:
        return default_window


def __validate_count(count):
    default_count = 1
    if count > 0:
        return count
    else:
        return default_count


def __get_score(window, new_doc, doc):
    set1 = set(new_doc.tokens)
    set2 = set(doc.tokens)
    total1 = __calculate_score(window, new_doc.tokens, set1, doc.tokens, set2)
    total2 = __calculate_score(window, doc.tokens, set2, new_doc.tokens, set1)

    return (total1 + total2) / (len(set1) + len(set2))


def __calculate_score(window, tokens1, set1, tokens2, set2):
    total = 0
    for s1 in set1:
        sentence1 = __generate_window(window, tokens1, s1)
        syn1 = lesk(sentence1, s1)
        max = 0
        for s2 in set2:
            sentence2 = __generate_window(window, tokens2, s2)
            syn2 = lesk(sentence2, s2)
            if syn1 is not None:
                if syn2 is not None:
                    sim = syn1.path_similarity(syn2)
                    if sim is not None and sim > max:
                        max = sim
        total += max
    return total


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

    return " ".join(new_tokens)
