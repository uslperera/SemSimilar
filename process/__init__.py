import logging
from model import Document

logging.basicConfig(level=logging.DEBUG)

def process(document):
    logging.info("Started process")


if __name__ == '__main__':
    process()