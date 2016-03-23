import multiprocessing
import threading
import json
from core.model.document import Document
from core.textprocessor.tokenize import CodeTokenizer
import timeit
from core.model.document_worker import parallel_process

with open('data/100posts.json') as posts_file:
    posts = json.loads(posts_file.read())

new_posts = posts[:1000]
Document.set_tokenizer(CodeTokenizer())
final_documents, final_texts = parallel_process(new_posts, 3)
print len(final_documents), len(final_texts)


"""
lock = multiprocessing.Lock()


def append_documents(documents, texts, final_documents, final_texts):
    lock.acquire()
    final_documents.extend(documents)
    final_texts.extend(texts)
    lock.release()


def worker(num):
    i = 0
    while True:
        i += 1
    print 'Worker:', num
    return


def worker1(posts, final_documents, final_texts):
    documents = []
    for post in posts:
        documents.append(Document(post['Id'], post['Title'], post['Body'], post['Tags']))

    texts = []
    for doc in documents:
        texts.append(" ".join(doc.get_stemmed_tokens()))

    # print(len(documents))
    append_documents(documents, texts, final_documents, final_texts)
    return


if __name__ == '__main__':
    start = timeit.default_timer()
    c = multiprocessing.cpu_count()
    print(c)
    c -= 1
    with open('data/100posts.json') as posts_file:
        # with open('data/posts.json') as posts_file:
        posts = json.loads(posts_file.read())

    print(len(posts))
    new_posts = posts[:118797]

    corpus_size = len(new_posts)
    jobs = []
    Document.set_tokenizer(CodeTokenizer())

    manager = multiprocessing.Manager()
    final_documents = manager.list()
    final_texts = manager.list()

    for i in range(c):
        if i == c - 1:
            # print((corpus_size / c) * i, (i + 1) * (corpus_size / c) + corpus_size % c)
            posts = new_posts[(corpus_size / c) * i:(i + 1) * (corpus_size / c) + corpus_size % c]
        else:
            # print((corpus_size / c) * i, (i + 1) * (corpus_size / c))
            posts = new_posts[(corpus_size / c) * i:(i + 1) * (corpus_size / c)]
        p = multiprocessing.Process(target=worker1, args=(posts, final_documents, final_texts))
        jobs.append(p)
        p.start()

    for job in jobs:
        job.join()

    print len(final_documents)
    stop = timeit.default_timer()
    print(stop - start)

    # i = 0
    # A = new_posts[i:i + 1000 / c]
    # i += 1000 / c
    # B = new_posts[i:i + 1000 / c]
    # i += 1000 / c
    # C = new_posts[i:i + 1000 / c + 1000 % c]
    #
    # print len(A), len(B), len(C)
    # print new_posts[0], new_posts[999]
    # print A[0], C[333]

    # jobs = []
    # for i in range(c):
    #     p = multiprocessing.Process(target=worker, args=(i,))
    #     jobs.append(p)
    #     p.start()

# !/usr/bin/python
'''
import thread
import time

# Define a function for the thread
def print_time( threadName, delay):
   count = 0
   while True:
      # time.sleep(delay)
      count += 1
      # print "%s: %s" % ( threadName, time.ctime(time.time()) )

# Create two threads as follows
try:
   thread.start_new_thread( print_time, ("Thread-1", 2, ) )
   thread.start_new_thread( print_time, ("Thread-2", 4, ) )
   thread.start_new_thread( print_time, ("Thread-2", 4, ) )
   thread.start_new_thread( print_time, ("Thread-2", 4, ) )
   thread.start_new_thread( print_time, ("Thread-2", 4, ) )
   thread.start_new_thread( print_time, ("Thread-2", 4, ) )
   thread.start_new_thread( print_time, ("Thread-2", 4, ) )
   thread.start_new_thread( print_time, ("Thread-2", 4, ) )
   thread.start_new_thread( print_time, ("Thread-2", 4, ) )
   thread.start_new_thread( print_time, ("Thread-2", 4, ) )
   thread.start_new_thread( print_time, ("Thread-2", 4, ) )
   thread.start_new_thread( print_time, ("Thread-2", 4, ) )
   thread.start_new_thread( print_time, ("Thread-2", 4, ) )
except:
   print "Error: unable to start thread"

while 1:
   pass
'''
"""
