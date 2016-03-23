# from core.similarity.knowledge import lesk as lesk

def ss_similarity(documents, new_document, hal_model, count):
    """Find documents using SemSimilar similarity.

    Both HAL and Lesk based similarity calculations are used to find the most related documents.

    :param documents: documents list
    :param new_document: document to search
    :param hal_model: HAL model created from existing documents
    :param count: number of results wanted
    :type documents: list<semsimilar.core.model.document.Document>
    :type new_document: semsimilar.core.model.document.Document 
    :type hal_model: semsimilar.core.similarity.corpus.hal.Hal
    :type count: int
    :returns: Top matched documents with their scores (0-1)
    :rtype: list<(semsimilar.core.model.document.Document, float)>

    :Example:
    
    >>> doc = Document(101, "PHP Session Security", 
        "What are some guidelines for maintaining 
        responsible session security with PHP", 
        "<security><php>")
    >>> ss_similarity(documents, doc, hal, 1)
    [(document, 0.708)]
    """
    # results_topic = hal_model.search(new_document.get_stemmed_tokens())
    # results_ontology = []
    # if results_topic:
    #     topic_document_ids, scores = zip(*results_topic)

    #     topic_documents = []
    #     for topic_document_id in topic_document_ids:
    #         topic_documents.append(documents[topic_document_id])

    #     results_ontology = lesk.ss_similarity(documents=topic_documents, new_document=new_document, count=count)

    # return results_ontology[:count]
    return
