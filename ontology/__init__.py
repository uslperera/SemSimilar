from nltk.wsd import lesk
import operator
from textprocessor import Processor
from model import Result


class Similarity(object):
    title_enabled = True
    description_enabled = False
    tags_enabled = False
    __window = 4
    __count = 1
    __documents = None
    __text_processor = Processor()

    def __init__(self, documents):
        self.__documents = documents

    @property
    def window(self):
        return self.__window

    @window.setter
    def window(self, window_size):
        if window_size > 1 & window_size % 2 == 0:
            self.__window = window_size

    @property
    def count(self):
        return self.__count

    @count.setter
    def count(self, count):
        if count > 0:
            self.__count = count

    def top(self, new_document):
        results = []
        for document in self.__documents:
            score = self.__similarity(new_document, document)
            if len(results) < self.__count:
                result = Result()
                result.score = score
                result.document = document
                results.append(result)
                if len(results) == self.__count:
                    results.sort(key=operator.attrgetter('score'), reverse=True)
            else:
                if results[self.__count - 1].score < score:
                    results.pop()
                    result = Result()
                    result.score = score
                    result.document = document
                    results.append(result)
                    results.sort(key=operator.attrgetter('score'), reverse=True)
        return results

    def __similarity(self, new_doc, doc):
        set1 = set(new_doc.tokens)
        set2 = set(doc.tokens)
        print(set1)
        print(set2)
        print(set1 & set2)
        total1 = self.__calculate_score(new_doc.tokens, set1, doc.tokens, set2)
        total2 = self.__calculate_score(doc.tokens, set2, new_doc.tokens, set1)

        return (total1 + total2) / (len(set1) + len(set2))

    def __calculate_score(self, tokens1, set1, tokens2, set2):
        total = 0
        for s1 in set1:
            sentence1 = self.__generate_window(tokens1, s1)
            syn1 = lesk(sentence1, s1)
            max = 0
            for s2 in set2:
                sentence2 = self.__generate_window(tokens2, s2)
                syn2 = lesk(sentence2, s2)
                if syn1 is not None:
                    if syn2 is not None:
                        sim = syn1.path_similarity(syn2)
                        if sim is not None and sim > max:
                            max = sim
            total += max
        return total

    def __generate_window(self, tokens, target):
        new_tokens = []
        index = tokens.index(target)
        right = 0
        if len(tokens) < self.__window + 1:
            return " ".join(tokens)
        # if index of the target word is greater than or equal to half of the windows size
        if index >= (self.__window / 2):
            left = index - (self.__window / 2)
        else:
            left = 0
            right = (self.__window / 2) - index
        # if index of the target
        if (index + right + (self.__window / 2)) < len(tokens):
            right = index + right + (self.__window / 2) + 1
        else:
            right = len(tokens)
            left -= (index + (self.__window / 2) + 1) - len(tokens)
        for num in range(left, right):
            new_tokens.append(tokens[num])

        return " ".join(new_tokens)
