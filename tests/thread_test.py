import multiprocessing
import threading
import json
from semsimilar.model.document import Document
from semsimilar.textprocessor.tokenize import CodeTokenizer
import timeit
from semsimilar.model.document_worker import parallel_process
import pickle
from semsimilar.similarity.corpus.hal import *
from semsimilar.similarity.main import ss_similarity

# post_links = []
post_links = {}

spec = ['p', '&#xa', '&#xd', 'pre', 'code', 'blockquote', 'strong', 'ul', 'li', 'a', 'href', 'em']


def load_post_links():
    with open('data/1000ids.json') as postlinks_file:
        postlinks = json.loads(postlinks_file.read())

    for i, p in enumerate(postlinks):
        # if i == 100:
        #     break

        if not post_links.has_key(int(p['PostId'])):
            post_links[int(p['PostId'])] = int(p['RelatedPostId'])
        elif isinstance(post_links[int(p['PostId'])], list):
            post_links[int(p['PostId'])].append(int(p['RelatedPostId']))
        else:
            temp = post_links[int(p['PostId'])]
            post_links[int(p['PostId'])] = [temp]
            post_links[int(p['PostId'])].append(int(p['RelatedPostId']))
            # l = ((int(p['PostId'])), int(p['RelatedPostId']))
            # post_links.append(l)


def search_post_link(dup_p, ori_p):
    for plink in post_links:
        dp, op = plink
        if op == int(ori_p) and dp == int(dup_p):
            return True
    return False


def test(count):
    with open('data/100posts.json') as posts_file:
    # with open('data/posts.json') as posts_file:
        posts = json.loads(posts_file.read())

    new_posts = posts[:1000]
    posts = None
    documents, final_texts = parallel_process(new_posts, 3)

    new_posts = None
    # pickle.dump(final_documents, open('temp/final_documents.p', 'wb'), pickle.HIGHEST_PROTOCOL)
    # pickle.dump(final_texts, open('temp/final_texts.p', 'wb'), pickle.HIGHEST_PROTOCOL)
    hal = HAL(final_texts)
    # hal.threshold = 0.7
    print len(documents), len(final_texts)

    final_texts = None

    # with open('data/100duplicates.json') as posts_file:
    with open('data/duplicates.json') as posts_file:
        duplicate_posts = json.loads(posts_file.read())

    duplicate_documents = []
    for i, post in enumerate(duplicate_posts):
        if i == count:
            break
        d = Document(post['Id'], post['Title'], post['Body'], post['Tags'])
        d.remove_special_words(spec)
        duplicate_documents.append(d)
        # duplicate_documents.append(Document(post['Id'], post['Title'], post['Body'], post['Tags']))

    duplicate_posts = None

    corrects = 0
    a = []
    print("--querying--")
    for doc in duplicate_documents:
        o_corrects = corrects
        start = timeit.default_timer()
        results = ss_similarity(documents, doc, hal, 10)
        end = timeit.default_timer()
        for top_doc, score in results:
            if post_links.has_key(int(doc.id)):
                if isinstance(post_links[int(doc.id)], list):
                    for id in post_links[int(doc.id)]:
                        if id == int(top_doc.id):
                            corrects += 1
                            break
                elif post_links[int(doc.id)] == int(top_doc.id):
                    corrects += 1

        # qtm = hal.convert_to_vector_space(doc.stemmed_tokens)
        # # results = hal.temp_search(doc.stemmed_tokens, qtm)
        # results = hal.keyword_search(doc.stemmed_tokens, qtm)
        # for top_d, score in results[:10]:
        #     top_doc = documents[top_d]
        #     if post_links.has_key(int(doc.id)):
        #         if isinstance(post_links[int(doc.id)], list):
        #             for id in post_links[int(doc.id)]:
        #                 if id == int(top_doc.id):
        #                     corrects += 1
        #                     break
        #         elif post_links[int(doc.id)] == int(top_doc.id):
        #             corrects += 1

        if o_corrects == corrects:
            b = (doc.id, doc.title)
            a.append(b)

    print(corrects)
    print(a)
    print(end - start)


if __name__ == '__main__':
    Document.set_tokenizer(CodeTokenizer())
    Document.description_enabled = True
    Document.tags_enabled = True
    load_post_links()
    test(1)
    # with open('data/100posts.json') as posts_file:
    #     posts = json.loads(posts_file.read())
    #
    #
    # for i, post in enumerate(posts):
    #     if i==1:
    #         break
    #     d = Document(post['Id'], post['Title'], post['Body'], post['Tags'])
    #     d.remove_special_words(spec)
    #     print(d.tokens)

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
