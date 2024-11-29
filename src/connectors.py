from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv()) # read local .env file

import os

from langchain_openai import AzureOpenAIEmbeddings, ChatOpenAI
from langchain_chroma import Chroma 

class Connectors:
    """Singleton class to hold these clients.
    """

    __embeddings_client = None
    __llm_client = None
    __vectorstore_client = None

    @classmethod
    def get_embeddings_client(cls):
        if cls.__embeddings_client == None:
            print('Creating embeddings client')
            cls.__embeddings_client = AzureOpenAIEmbeddings(
                model='text-embedding-3-large',
                azure_endpoint = os.getenv('AZURE_OPENAI_EMBEDDINGS_ENDPOINT'),
                api_version= os.getenv('AZURE_OPENAI_EMBEDDINGS_API_VERSION')
            )
        return cls.__embeddings_client
    
    @classmethod
    def get_llm_client(cls):
        if cls.__llm_client == None:
            print('Creating llm client')
            cls.__llm_client = ChatOpenAI(
                model="gpt-4o-mini",
                api_key=os.getenv('OPENAI_API_KEY')
            )
        return cls.__llm_client
    
    @classmethod
    def get_vectorstore_client(cls):
        if cls.__vectorstore_client == None:
            print('Creating vectorstore client')
            embedding = cls.get_embeddings_client()
            cls.__vectorstore_client = Chroma(
                embedding_function=embedding,
                persist_directory='vectorstore/'
            )
        return cls.__vectorstore_client