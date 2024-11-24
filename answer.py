from langchain_openai import ChatOpenAI
import os
from langchain.vectorstores import Chroma 
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv()) # read local .env file

from langchain_openai import AzureOpenAIEmbeddings
embedding = AzureOpenAIEmbeddings(
    model='text-embedding-3-large',
    azure_endpoint = os.getenv('AZURE_OPENAI_EMBEDDINGS_ENDPOINT'),
    api_version= os.getenv('AZURE_OPENAI_EMBEDDINGS_API_VERSION')
)

llm = ChatOpenAI(
    model="gpt-4o",
    api_key=os.getenv('OPENAI_API_KEY')
)

vectorstore = Chroma(
    embedding_function=embedding,
    persist_directory='vectorstore/'
)
retriever = vectorstore.as_retriever()


# 2. Incorporate the retriever into a question-answering chain.
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

system_prompt = (
    "You are an assistant for question-answering tasks. "
    "Use the following pieces of retrieved context to answer "
    "the question. If you don't know the answer, say that you "
    "don't know. Use three sentences maximum and keep the "
    "answer concise."
    "\n\n"
    "{context}"
)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
)

question_answer_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)



while True:
    print()
    print()
    query = input("Enter query:  ")

    result = rag_chain.invoke({"input": query})


    ans = result['answer']
    context_documents = result['context']

    print(f'ANSWER: {ans}')
    print()
    print('CONTEXT:')
    for document in context_documents:
        chap = document.metadata['chapter']
        subchap = document.metadata['subchapter']
        print(f'Chapter: {chap}, subheading: {subchap}')
