# SCRIPT
# Reads the word document (python-docx) and ingests knowledge (Chapter 2 - 17 inclusive, ignores questions and answers), 
# and creates vectorstore.

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv()) # read local .env file

import os

from langchain.vectorstores import Chroma 
from langchain.schema.document import Document

from data_extraction import read_doc
from src.connectors import Connectors


doc_tree = read_doc.get_document_tree(os.path.join("data","ATPL Ground Training Series - Book 8 Human Performance and Limitations MCQ CORRECTED.docx"))
doc_tree = doc_tree[:-2] # ignore chapters 18 - specimen questions, and onwards
# doc_tree = doc_tree[1:3]


chunks: list[Document] = []
for chapter in doc_tree:
    for heading3 in chapter.contents:
        chunk = Document(
            page_content=f'Chapter: {chapter.name}, Sub-chapter: {heading3.name}, '
        )
        markdown = f"# {chapter.name}\n"
        markdown += f"## {heading3.name}\n"
        leaves = heading3.get_leaves()
        current_heading4 = ''
        for leaf in leaves:
            text = ''
            if leaf.parent.level == 'Heading 4' and leaf.parent.name != current_heading4:
                current_heading4 = leaf.parent.name
                if current_heading4 != '':
                    text += f'\n\n### {leaf.parent.name}: \n'
                else: 
                    text += '\n\n'
            elif leaf.parent.level == 'Heading 4' and leaf.parent.name == current_heading4:
                pass
            else:
                current_heading4 = ''
                text += '\n\n'

            text += leaf.name + '\n'
            chunk.page_content += text
            markdown += text
        chunk.metadata = {
            'chapter': chapter.name,
            'subchapter': heading3.name,
            'markdown': markdown
        }
        chunks.append(chunk)

for chunk in chunks:
    print('\033[32mCHUNK:\033[0m')
    print(chunk.page_content)
    print()
    print()
    print()

vectordb = Chroma.from_documents(
    documents=chunks,
    embedding=Connectors.get_embeddings_client(),
    persist_directory='vectorstore/'
)
print(vectordb._collection.count())
