API
************************
Models
===================
Document
----------------
.. autoclass:: document.Document
	:members:

Here is an example::
	
    Document(101, "PHP Session Security", 
    "What are some guidelines for maintaining 
    responsible session security with PHP",
     "<security><php>")


Document Worker
----------------
.. automodule:: document_worker
	:members: parallel_process

Here is an example::

	final_documents, final_texts = parallel_process(new_posts, 3)

Text Processors
===================
CodeTokenizer
----------------
.. autoclass:: tokenize.CodeTokenizer
	:members: tokenize

.. note:: Compatible with any tokenizer extending **nltk.tokenize.api.TokenizerI**


Other
----------------
.. automodule:: processor
	:members:

.. automodule:: wsd
	:members: get_synsets

Semantic Similarity
===================
.. automodule:: lesk
	:members: 

Here is an example::

	results_ontology = lesk.similarity(documents=topic_documents, 
	new_document=new_document, count=count)

.. autoclass:: hal.HAL
	:members:

Here is an example::

	hal = HAL(documents=final_texts)

.. automodule:: main
	:members:

Here is an example::

	similarity(documents, doc, hal, 5)