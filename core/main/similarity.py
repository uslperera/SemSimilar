import core.ontology
import core.topicmodel
from core.model import Result

import operator


class Similarity(object):
    __ontology = core.ontology.Similarity
    __topic = core.topicmodel.Similarity
    __count = 1

    def __init__(self, documents, dictionary, corpus, ldamodel):
        self.__ontology = core.ontology.Similarity(documents)
        self.__topic = core.topicmodel.Similarity(ldamodel, dictionary, corpus, documents)

    @property
    def count(self):
        return self.__count

    @count.setter
    def count(self, count):
        if count > 0:
            self.__count = count
            self.__ontology.count = count
            self.__topic.count = count

    def top(self, new_document):

        results_ontology = self.__ontology.top(new_document)
        results_topic = self.__topic.top(new_document)

        ids_ontology = []
        for r in results_ontology:
            ids_ontology.append(r.document.id)

        ids_topics = []
        for r in results_topic:
            ids_topics.append(r.document.id)

        results_combined = set(ids_ontology) | set(ids_topics)

        results = []
        for r in results_combined:
            score = 0
            document = None
            for rt in results_topic:
                if r == rt.document.id:
                    score += rt.score
                    document = rt.document
                    break
            for ro in results_ontology:
                if r == ro.document.id:
                    document = ro.document
                    score += ro.score
                    break
            score /= 2
            result = Result()
            result.score = score
            result.document = document
            results.append(result)

        results.sort(key=operator.attrgetter('score'), reverse=True)
        return results[:self.__count]
