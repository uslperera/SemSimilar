from core.ontology import lesk_similarity as lesk
from core.topicmodel import lda_similarity as lda


def similarity(documents, new_document, count, lda_model, dictionary, corpus):
    results_topic = lda.similarity(lda_model=lda_model, dictionary=dictionary, corpus=corpus, documents=documents,
                                   new_document=new_document, count=10)
    results_ontology = []
    if results_topic:
        topic_documents, scores = zip(*results_topic)

        topic_documents = list(topic_documents)

        results_ontology = lesk.similarity(documents=topic_documents, new_document=new_document, count=count)

    # results_ontology.sort(key=lambda tup: tup[1], reverse=True)
    return results_ontology[:count]
