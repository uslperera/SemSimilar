import json

from gensim import models, corpora

from semsimilar.model import Document
from semsimilar.model.document_worker import parallel_process
from semsimilar.similarity_core.main import *
from semsimilar.textprocessor.tokenize import CodeTokenizer
from semsimilar.similarity_core.corpus.hal import *
from nltk.tokenize import RegexpTokenizer
import pickle

tokenizer = RegexpTokenizer(r'<(.*?)\>')

# post_links = []
post_links = {}


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


def test(count, tag_count):
    with open('data/100posts.json') as posts_file:
        posts = json.loads(posts_file.read())

    documents = []
    for i, post in enumerate(posts):
        if i == count:
            break
        documents.append(Document(post['Id'], post['Title'], post['Body'], post['Tags']))

    # documents = pickle.load(open('temp/documents.p', 'rb'))
    print("a")
    texts = []
    for doc in documents:
        texts.append(doc.get_stemmed_tokens())

    print("b")
    dictionary = corpora.Dictionary(texts)
    print("c")
    corpus = [dictionary.doc2bow(text) for text in texts]
    print("d")
    tfidf = models.TfidfModel(corpus)
    tfidf_corpus = tfidf[corpus]
    print("e")
    # ldamodel = models.ldamodel.LdaModel(tfidf_corpus, id2word=dictionary, num_topics=tag_count)
    # ldamodel = models.LdaMulticore(workers=3, corpus=tfidf_corpus, id2word=dictionary, num_topics=tag_count)
    ldamodel = models.wrappers.LdaMallet('/Users/shamal/Downloads/mallet-2.0.7/bin/mallet', corpus=tfidf_corpus,
                                         num_topics=tag_count,
                                         id2word=dictionary)
    # ldamodel = models.HdpModel(tfidf_corpus, dictionary)
    print("f")
    # ldamodel.update(tfidf_corpus)
    # ldamodel.save('temp/lda2.model')

    # ldamodel = models.LdaModel.load("temp/lda2.model")
    print("g")
    with open('data/100duplicates.json') as posts_file:
        duplicate_posts = json.loads(posts_file.read())

    duplicate_documents = []
    for i, post in enumerate(duplicate_posts):
        if i == 2:
            break
        duplicate_documents.append(Document(post['Id'], post['Title'], post['Body'], post['Tags']))

    print("h")
    print(len(duplicate_documents))
    corrects = 0
    a = []
    for doc in duplicate_documents:
        results = ss_similarity(lda_model=ldamodel, dictionary=dictionary, corpus=tfidf_corpus, documents=documents,
                                new_document=doc, count=2)
        # print(results)
        for top_doc, score in results:
            if top_doc is not None:
                print(doc.id, doc.title, top_doc.id, top_doc.title, score)
                # if search_post_link(doc.id, top_doc.id):
                #     corrects += 1
                # else:
                #     b = (doc.id, top_doc.id)
                #     a.append(b)
                if post_links[int(doc.id)] == int(top_doc.id):
                    corrects += 1

    print(corrects)
    print a


def get_tags(count):
    # 12404
    with open('data/100posts.json') as posts_file:
        posts = json.loads(posts_file.read())

    str = ""
    for i, post in enumerate(posts):
        # if i == count:
        #     break
        str += post['Tags']

    docs = tokenizer.tokenize(str)
    # print(docs)

    s1 = set(docs)
    # print(s1)

    return len(s1)


def print_topics(count):
    with open('data/100posts.json') as posts_file:
        posts = json.loads(posts_file.read())

    documents = []
    for i, post in enumerate(posts):
        if i == count:
            break
        documents.append(Document(post['Id'], post['Title'], post['Body'], post['Tags']))

    for doc in documents:
        print(doc.title)


def test_hal(count):
    doc_m = {}
    with open('data/100posts.json') as posts_file:
        # with open('data/posts.json') as posts_file:
        posts = json.loads(posts_file.read())

    documents = []
    for i, post in enumerate(posts):
        if i == count:
            break
        documents.append(Document(post['Id'], post['Title'], post['Body'], post['Tags']))
        # doc_m[int(post['Id'])] = i

    print(len(documents))

    texts = []
    for doc in documents:
        texts.append(" ".join(doc.get_stemmed_tokens()))

    hal = HAL(documents=texts)

    with open('data/100duplicates.json') as posts_file:
        # with open('data/duplicates.json') as posts_file:
        duplicate_posts = json.loads(posts_file.read())

    duplicate_documents = []
    for i, post in enumerate(duplicate_posts):
        if i == count:
            break
        duplicate_documents.append(Document(post['Id'], post['Title'], post['Body'], post['Tags']))

    corrects = 0
    a = []
    print("--querying--")
    for doc in duplicate_documents:
        o_corrects = corrects
        results = hal.search(doc.get_stemmed_tokens())
        results = results[:5]
        for top_doc, score in results:
            print(doc.title, documents[top_doc].title, score)
            if post_links.has_key(int(doc.id)):
                if isinstance(post_links[int(doc.id)], list):
                    for id in post_links[int(doc.id)]:
                        if id == int(documents[top_doc].id):
                            corrects += 1
                            break
                elif post_links[int(doc.id)] == int(documents[top_doc].id):
                    corrects += 1

                    # if o_corrects == corrects:
                    #     b = (doc.id, doc.title)
                    #     a.append(b)

    print(corrects)
    print a


def test_final(count):
    doc_m = {}
    with open('data/100posts.json') as posts_file:
        # with open('data/posts.json') as posts_file:
        posts = json.loads(posts_file.read())

    # documents = []
    # for i, post in enumerate(posts):
    #     if i == count:
    #         break
    #     documents.append(Document(post['Id'], post['Title'], post['Body'], post['Tags']))

    documents, texts = parallel_process(posts[:1000], 3)
    # print(len(documents))

    # texts = []
    # for doc in documents:
    #     texts.append(" ".join(doc.stemmed_tokens))
    #
    hal = HAL(documents=texts)


    with open('data/100duplicates.json') as posts_file:
        duplicate_posts = json.loads(posts_file.read())

    duplicate_documents = []
    for i, post in enumerate(duplicate_posts):
        if i == count:
            break
        duplicate_documents.append(Document(post['Id'], post['Title'], post['Body'], post['Tags']))

    corrects = 0
    a = []
    print("--querying--")
    for doc in duplicate_documents:
        o_corrects = corrects
        # results = ss_similarity(documents, doc, hal, 5)
        results = ss_similarity(documents, doc, hal, 5)
        for top_doc, score in results:
            # print(doc.id, doc.title, top_doc.id, top_doc.title, score)
            if post_links.has_key(int(doc.id)):
                if isinstance(post_links[int(doc.id)], list):
                    for id in post_links[int(doc.id)]:
                        if id == int(top_doc.id):
                            corrects += 1
                            break
                elif post_links[int(doc.id)] == int(top_doc.id):
                    corrects += 1

                    # if o_corrects == corrects:
                    #     b = (doc.id, doc.title)
                    #     a.append(b)

    print(corrects)
    print a

def aa():
    with open('data/100posts.json') as posts_file:
        posts = json.loads(posts_file.read())

    new_posts = posts[:1000]
    Document.set_tokenizer(CodeTokenizer())
    final_documents, final_texts = parallel_process(new_posts, 3)
    # pickle.dump(final_documents, open('temp/final_documents.p', 'wb'), pickle.HIGHEST_PROTOCOL)
    # pickle.dump(final_texts, open('temp/final_texts.p', 'wb'), pickle.HIGHEST_PROTOCOL)
    h = HAL(final_texts)

import timeit
if __name__ == '__main__':
    Document.set_window(4)
    Document.tags_enabled = True
    # Document.description_enabled = True
    Document.set_tokenizer(CodeTokenizer())
    load_post_links()
    # tag_count = get_tags(100)
    # print tag_count
    # test(100, 20)
    # print(post_links)
    # print_topics(20)
    test_hal(200)
    start = timeit.default_timer()
    stop = timeit.default_timer()
    print(stop - start)
    """
        122
        []
        200
        --querying--
        154
        []
    """