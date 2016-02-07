import json
from core.model import Document
from core.textprocessor.document_builder import process
from core.ontology import lesk_similarity as lesk
import pickle


'''
# Read all the documents from the data source
posts = []
with open('data/posts1.json') as posts_file:
    posts = json.loads(posts_file.read())

documents = []
for post in posts:
    documents.append(Document(post['Id'], post['Title'], post['Body'], post['Tags']))

# Tokenize the documents

try:
    process(documents=documents, title_enabled=True, description_enabled=False, tags_enabled=True, window=0)
finally:
    pickle.dump(documents, open('temp/documents.p', 'wb'), pickle.HIGHEST_PROTOCOL)
'''


documents = pickle.load(open('temp/documents.p', 'rb'))

# Read all the new documents
duplicate_posts = []
with open('data/duplicates1.json') as posts_file:
    duplicate_posts = json.loads(posts_file.read())

duplicate_documents = []
i = 0
for post in duplicate_posts:
    if i < 50:
        duplicate_documents.append(Document(post['Id'], post['title'], post['body'], post['tags']))
    i += 1

# Tokenize the documents
new_docs_builder = process(documents=duplicate_documents, title_enabled=True, description_enabled=False,
                           tags_enabled=True, window=0)

# Ontology similarity
count = 2
for doc in duplicate_documents:
    if doc is not None:
        results = lesk.similarity(documents=documents, new_document=doc, count=0)
        for top_doc, score in results:
            if top_doc is not None:
                print(doc.id, doc.title, top_doc.id, top_doc.title, score)
