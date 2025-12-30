import os

from openai import OpenAI

from src import config


class Embeddings:

    __client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    
    @classmethod
    def embed_texts(cls, texts: list[str]) -> list[list[float]]:
        response = cls.__client.embeddings.create(
            input=texts,
            model=config.EMBEDDING_MODEL
        )

        embeddings_results = response.data
        embeddings = []
        for result in embeddings_results:
            embeddings.append(result.embedding)
        return embeddings