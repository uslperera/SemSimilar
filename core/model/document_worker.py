import multiprocessing
from core.model.document import Document

lock = multiprocessing.Lock()


def append_documents(documents, texts, final_documents, final_texts):
    lock.acquire()
    final_documents.extend(documents)
    final_texts.extend(texts)
    lock.release()


def worker(posts, final_documents, final_texts):
    documents = []
    for post in posts:
        documents.append(Document(post['Id'], post['Title'], post['Body'], post['Tags']))

    texts = []
    for doc in documents:
        texts.append(" ".join(doc.get_stemmed_tokens()))

    append_documents(documents, texts, final_documents, final_texts)
    return


def parallel_process(posts, processors):
    if processors > multiprocessing.cpu_count():
        # throw exception
        a = "exp"
    else:
        corpus_size = len(posts)
        jobs = []

        manager = multiprocessing.Manager()
        final_documents = manager.list()
        final_texts = manager.list()

        for i in range(processors):
            if i == processors - 1:
                temp_posts = posts[
                             (corpus_size / processors) * i:(i + 1) * (corpus_size / processors) + corpus_size % processors]
            else:
                temp_posts = posts[(corpus_size / processors) * i:(i + 1) * (corpus_size / processors)]
            p = multiprocessing.Process(target=worker, args=(temp_posts, final_documents, final_texts))
            jobs.append(p)
            p.start()

        for job in jobs:
            job.join()

        result = (final_documents, final_texts)
        return result