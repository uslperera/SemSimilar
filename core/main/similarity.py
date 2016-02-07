from core.ontology import lesk_similarity as lesk
from core.topicmodel import lda_similarity as lda


def similarity(documents, new_document, count, lda_model, dictionary, corpus):
    results_ontology = lesk.similarity(documents=documents, new_document=new_document, count=count)
    results_topic = lda.similarity(lda_model=lda_model, dictionary=dictionary, corpus=corpus, documents=documents,
                                   new_document=new_document, count=count)

    ids_ontology = []
    for document, score in results_ontology:
        ids_ontology.append(document.id)

    ids_topics = []
    for document, score in results_topic:
        ids_topics.append(document.id)

    results_combined = set(ids_ontology) | set(ids_topics)

    results = []
    for r in results_combined:
        score = 0
        document = None
        for document, score in results_topic:
            if r == document.id:
                score += score
                document = document
                break
        for document, score in results_ontology:
            if r == document.id:
                document = document
                score += score
                break
        score /= 2
        result = (document, score)
        results.append(result)

    results.sort(key=lambda tup: tup[1], reverse=True)
    return results[:count]
