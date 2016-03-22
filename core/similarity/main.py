from core.similarity.knowledge import lesk as lesk
import sys
import logging

def similarity(documents, new_document, hal_model, count):
    """Get semantically similar documents"""
    try:
        results_topic = hal_model.search(new_document.stemmed_tokens)
        results_ontology = []
        if results_topic:
            topic_document_ids, scores = zip(*results_topic)

            topic_documents = []
            for topic_document_id in topic_document_ids:
                topic_documents.append(documents[topic_document_id])

            results_ontology = lesk.similarity(documents=topic_documents, new_document=new_document, count=count)
    except:
        e = sys.exc_info()[0]
        logging.error(e)
    return results_ontology[:count]
