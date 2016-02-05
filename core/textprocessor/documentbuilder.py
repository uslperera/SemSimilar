from core.textprocessor import processor


def process(documents, title_enabled, description_enabled, tags_enabled):
    for document in documents:
        if title_enabled & description_enabled & tags_enabled:
            text = document.title + " " + document.description + " " + document.tags
        elif title_enabled & description_enabled:
            text = document.title + " " + document.description
        elif title_enabled & tags_enabled:
            text = document.title + " " + document.tags
        else:
            text = document.title

        tokens = processor.process(text)
        document.tokens = tokens
