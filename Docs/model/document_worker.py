# import multiprocessing
# from core.model.document import Document

# lock = multiprocessing.Lock()


def append_documents(documents, texts, final_documents, final_texts):
    """Add documens to the array"""
    # lock.acquire()
    # final_documents.extend(documents)
    # final_texts.extend(texts)
    # lock.release()
    return


def worker(posts, final_documents, final_texts):
    """Worker process to process documents"""
    # documents = []
    # for post in posts:
    #     documents.append(Document(post['Id'], post['Title'], post['Body'], post['Tags']))

    # texts = []
    # for doc in documents:
    #     texts.append(" ".join(doc.get_stemmed_tokens()))

    # append_documents(documents, texts, final_documents, final_texts)
    return


def parallel_process(posts, processors):
    """Process large set of documents using parallel processing


    :param posts: posts, articles
    :param processors: number of processors
    :type posts: list<key-value object>
    :type processors: int
    :returns: Processed documents
    :rtype: list<semsimilar.core.model.document.Document>

    .. note:: Keys can be initialized before calling this function. (ID_KEY, TITLE_KEY, DESCRIPTION_KEY, TAGS_KEY)

    :Example:

    >>> with open('articles.json') as articles_file:
            articles = json.loads(articles_file.read())
    >>> parallel_process(articles, 2)
    """
    # if processors > multiprocessing.cpu_count():
    #     # throw exception
    #     a = "exp"
    # else:
    #     corpus_size = len(posts)
    #     jobs = []

    #     manager = multiprocessing.Manager()
    #     final_documents = manager.list()
    #     final_texts = manager.list()

    #     for i in range(processors):
    #         if i == processors - 1:
    #             temp_posts = posts[
    #                          (corpus_size / processors) * i:(i + 1) * (
    #                          corpus_size / processors) + corpus_size % processors]
    #         else:
    #             temp_posts = posts[(corpus_size / processors) * i:(i + 1) * (corpus_size / processors)]
    #         p = multiprocessing.Process(target=worker, args=(temp_posts, final_documents, final_texts))
    #         jobs.append(p)
    #         p.start()

    #     for job in jobs:
    #         job.join()

    #     result = (final_documents, final_texts)
    #     return result
    return
