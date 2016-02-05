from nltk.corpus import wordnet as wn


def similarity(documents, new_document, window, count):
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


def __validate_count(count):
    default_count = 1
    if count > 0:
        return count
    else:
        return default_count


def __get_score(window, new_doc, doc):
    set1 = set(new_doc.tokens)
    set2 = set(doc.tokens)
    total1 = __calculate_score(set(new_doc.synsets), set(doc.synsets))
    total2 = __calculate_score(set(doc.synsets), set(new_doc.synsets))

    return (total1 + total2) / (len(set1) + len(set2))


def __calculate_score(synsets1, synsets2):
    total = 0
    for syn1 in synsets1:
        max = 0
        if syn1 is not None:
            for syn2 in synsets2:
                if syn2 is not None:
                    sim = wn.synset(syn1).path_similarity(wn.synset(syn2))
                    if sim is not None and sim > max:
                        max = sim
        total += max
    return total
