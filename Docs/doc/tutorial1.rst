Getting Started
======================================

This tutorial will give you an idea on how to get semantically similar results using SemSimilar search.

::

	import json
	from semsimilar.core.model import Document
	from semsimilar.core.similarity.main import *
	from semsimilar.core.textprocessor.tokenize import CodeTokenizer
	from semsimilar.core.similarity.corpus.hal import *

	# Set tokenizer
	Document.set_tokenizer(CodeTokenizer())

	# Load data from a file
	with open('posts.json') as posts_file:
	    posts = json.loads(posts_file.read())

	# Create documents list
	documents = []
	for i, post in enumerate(posts):
	    documents.append(Document(post['Id'], post['Title'], post['Body'], post['Tags']))

	# Get stemmed tokens
	texts = []
	for doc in documents:
	    texts.append(" ".join(doc.get_stemmed_tokens()))

	# Create HAL model
	hal = HAL(documents=texts)

	search_document = Document(107, "New document", None, None)

	# Get best 5 documents
	results = ss_similarity(documents, search_document, hal, 5)

	__