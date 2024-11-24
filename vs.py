from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv()) # read local .env file
import os
from langchain.vectorstores import Chroma 

from langchain_openai import AzureOpenAIEmbeddings
embedding = AzureOpenAIEmbeddings(
    model='text-embedding-3-large',
    azure_endpoint = os.getenv('AZURE_OPENAI_EMBEDDINGS_ENDPOINT'),
    api_version= os.getenv('AZURE_OPENAI_EMBEDDINGS_API_VERSION')
)

from langchain.schema.document import Document
import read_doc

doc_tree = read_doc.get_document_tree('ATPL Ground Training Series - Book 8 Human Performance and Limitations.docx')
doc_tree = doc_tree[:-2] # ignore chapters 18 - specimen questions, and onwards
# doc_tree = doc_tree[1:3]


chunks: list[Document] = []
for chapter in doc_tree:
    for heading3 in chapter.contents:
        chunk = Document(
            page_content=f'Chapter: {chapter.name}, Sub-chapter: {heading3.name}, '
        )
        chunk.metadata = {
            'chapter': chapter.name,
            'subchapter': heading3.name
        }
        leaves = heading3.get_leaves()
        for leaf in leaves:
            text = leaf.name
            if leaf.parent.level == 'Heading 4':
                text = f'{leaf.parent.name}: ' + text
            text += '\n'
            chunk.page_content += text
        chunks.append(chunk)

for chunk in chunks:
    print('\033[32mCHUNK:\033[0m')
    print(chunk.page_content)
    print()
    print()
    print()

vectordb = Chroma.from_documents(
    documents=chunks,
    embedding=embedding,
    persist_directory='vectorstore/'
)
print(vectordb._collection.count())
