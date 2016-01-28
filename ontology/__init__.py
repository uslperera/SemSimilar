from nltk.corpus import wordnet as wn
from nltk.wsd import lesk
import operator
from textprocessor import Processor
from model import Result


class Similarity(object):
    title_enabled = True
    description_enabled = False
    tags_enabled = False
    window = 4
    __documents = None
    __textprocessor = Processor

    def __init__(self, documents):
        self.__documents = documents

    def top(self, new_document):
        count = 1
        results = []
        for document in self.__documents:
            score = self.similarity(new_document, document)
            if len(results) < count:
                result = Result()
                result.score = score
                result.document = document
                results.append(result)
                if(len(results) == count):
                    results.sort(key=operator.attrgetter('score'), reverse=True)
            else:
                if results[count-1].score < score:
                    results.pop()
                    result = Result()
                    result.score = score
                    result.document = document
                    results.append(result)
                    results.sort(key=operator.attrgetter('score'), reverse=True)
        #results.sort(key=operator.attrgetter('score'), reverse=True)
        return results

    def similarity(self, doc1, doc2):
        if self.title_enabled & self.description_enabled & self.tags_enabled:
            sent1 = doc1.title + doc1.description + doc1.tags
            sent2 = doc2.title + doc2.description + doc2.tags
        elif self.title_enabled & self.description_enabled:
            sent1 = doc1.title + doc1.description
            sent2 = doc2.title + doc2.description
        elif self.title_enabled & self.tags_enabled:
            sent1 = doc1.title + doc1.tags
            sent2 = doc2.title + doc2.tags
        else:
            sent1 = doc1.title
            sent2 = doc2.title

        tokens1 = self.__textprocessor.tokenize(sent1)
        tokens1 = self.__textprocessor.remove_stopwords(tokens1)
        tokens2 = self.__textprocessor.tokenize(sent2)
        tokens2 = self.__textprocessor.remove_stopwords(tokens2)
        set1 = set(tokens1)
        set2 = set(tokens2)
        total1 = self.calc_score(tokens1, set1, tokens2, set2)
        total2 = self.calc_score(tokens2, set2, tokens1, set1)

        return (total1 + total2) / (len(set1) + len(set2))

    def calc_score(self, tokens1, set1, tokens2, set2):
        total = 0
        for s1 in set1:
            sentence1 = self.generate_window(tokens1, s1)
            syn1 = lesk(sentence1, s1)
            max = 0
            for s2 in set2:
                sentence2 = self.generate_window(tokens2, s2)
                syn2 = lesk(sentence2, s2)
                if (syn1 is not None):
                    if (syn2 is not None):
                        sim = syn1.path_similarity(syn2)
                        if (sim != None):
                            if (sim > max):
                                max = sim
            total += max
        return total

    def generate_window(self, tokens, target):
        new_tokens = []
        index = tokens.index(target)
        left = 0
        right = 0
        if len(tokens)< self.window+1:
            return " ".join(tokens)
        #if index of the target word is greater than or equal to half of the windows size
        if(index>=(self.window/2)):
            left = index - (self.window/2)
        else:
            left = 0
            right = (self.window/2)-index
        #if index of the target
        if (index + right+ (self.window/2))<len(tokens):
            right = index + right + (self.window/2) + 1
        else:
            right = len(tokens)
            left = left - ((index+(self.window/2)+1)-len(tokens))
        for num in range(left, right):
            new_tokens.append(tokens[num])
        return " ".join(new_tokens)