import json
from core.model import Document
from core.textprocessor import DocumentsBuilder
from core.ontology import Similarity
from core.textprocessor import Processor

processor = Processor()

# Read all the documents from the data source
posts = []
with open('data/posts1.json') as posts_file:
    posts = json.loads(posts_file.read())

documents = []
for post in posts:
    documents.append(Document(post['Id'], post['Title'], post['Body'], post['Tags']))

# Tokenize the documents
docs_builder = DocumentsBuilder(documents)
docs_builder.tags_enabled = True
docs_builder.description_enabled = True
docs_builder.process()

# Read all the new documents
duplicate_posts = []
with open('data/duplicates.json') as posts_file:
    duplicate_posts = json.loads(posts_file.read())

duplicate_documents = []
i = 0
for post in duplicate_posts:
    if i < 50:
        duplicate_documents.append(Document(post['Id'], post['title'], post['body'], post['tags']))
    i += 1

# Tokenize the documents
new_docs_builder = DocumentsBuilder(duplicate_documents)
new_docs_builder.tags_enabled = True
new_docs_builder.description_enabled = True
new_docs_builder.process()

# Ontology similarity
s = Similarity(documents)
s.count = 2
for doc in duplicate_documents:
    if doc is not None:
        results = s.top(doc)
        for result in results:
            top_doc = result.document
            if top_doc is not None:
                print(doc.id, doc.title, top_doc.id, top_doc.title, result.score)
