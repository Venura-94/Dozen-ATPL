# SCRIPT
# Reads the word document (python-docx) and ingests knowledge (Chapter 2 - 17 inclusive, ignores questions and answers), 
# and creates vectorstore.

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv()) # read local .env file

import os
import json

from src.operators.read_word_doc import get_document_tree
from src.operators.document_tree_to_chunks import document_tree_to_chunks
from src.connectors.embeddings import Embeddings
from src.connectors.vectorstore import ChromaLocal


FILENAME = "ATPL Ground Training Series - Book 8 Human Performance and Limitations MCQ CORRECTED.docx"
FILEPATH = os.path.join("textbook_input", FILENAME)
BOOK_NAME = "book8"


blocks = get_document_tree(FILEPATH)
blocks = blocks[:-2] # ignore chapters 18 - specimen questions, and onwards

# write the textbook tree to a json file for visualization
os.makedirs("textbook_tree/", exist_ok=True)
blocks_as_dicts: list[dict] = []
for block in blocks:
    blocks_as_dicts.append(block.as_dict())
with open(f"textbook_tree/{BOOK_NAME}_tree.json", "wt") as f:
    json.dump(blocks_as_dicts, f, indent=2)

chunks = document_tree_to_chunks(tree=blocks, book_name=BOOK_NAME)

# embed the chunks
texts = []
for chunk in chunks: texts.append(chunk.markdown)
embeddings = Embeddings.embed_texts(texts)
for i, embedding in enumerate(embeddings):
    chunks[i].embedding = embedding

# add to vectorstore
collection_names = ChromaLocal.list_collections()
print(f"collection_names: {collection_names}")
if BOOK_NAME in collection_names: ChromaLocal.delete_collection(name=BOOK_NAME)
ChromaLocal.create_collection(name=BOOK_NAME)
ChromaLocal.add_to_collection(name=BOOK_NAME, chunks=chunks)

