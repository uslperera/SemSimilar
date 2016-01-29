import ontology.similarity
import topicmodel.similarity
from model import Document
from model import Result

import operator


class Similarity(object):
    __ontology = ontology.Similarity
    __topic = topicmodel.Similarity

    def __init__(self, documents, dictionary, tfidf_corpus, ldamodel):
        self.__ontology = ontology.Similarity(documents)
        self.__topic = topicmodel.Similarity(ldamodel, dictionary, tfidf_corpus, documents)

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
        return results
