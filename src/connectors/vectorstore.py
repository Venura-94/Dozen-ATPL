from uuid import uuid4

from chromadb import PersistentClient, Client

from src import config
from src.models.chunk import Chunk


class ChromaLocal:

    __chroma_client = PersistentClient(path="chroma_vectorstore")

    @classmethod
    def create_collection(cls, name: str):
        cls.__chroma_client.create_collection(name=name, configuration=config.CHROMA_COLLECTION_CONFIG)

    @classmethod
    def list_collections(cls) -> list[str]:
        collections = cls.__chroma_client.list_collections()
        names = []
        for collection in collections: names.append(collection.name)
        return names
    
    @classmethod
    def delete_collection(cls, name: str):
        cls.__chroma_client.delete_collection(name)

    @classmethod
    def add_to_collection(cls, name: str, chunks: list[Chunk]):

        # validate: check if every chunk has a vector of same length
        if len(chunks) == 0: return
        first_chunk = chunks[0]
        if first_chunk.embedding is None: raise ValueError("At least one chunk does not have an embedding")
        emb_length = len(first_chunk.embedding)
        for chunk in chunks:
            embedding = chunk.embedding
            if embedding is None: raise ValueError("At least one chunk does not have an embedding")
            if len(embedding) != emb_length: raise ValueError("At least one chunk's embedding has a different length")

        # prep the lists needed for adding to chroma vectorstore
        ids = []; embeddings = []; documents = []; metadatas = []
        for chunk in chunks:
            ids.append(str(uuid4()))
            embeddings.append(chunk.embedding)
            documents.append(chunk.markdown)
            metadatas.append(chunk.get_metadata())
        
        # add to chroma collection
        collection = cls.__chroma_client.get_collection(name)
        collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas,
        )

    @classmethod
    def query_collection(cls, collection_name: str, embedding: list[float], top_k = 4) -> list[Chunk]:
        collection = cls.__chroma_client.get_collection(collection_name)
        query_result = collection.query(query_embeddings=embedding, n_results=top_k)

        chunks_and_scores: list[tuple[Chunk, float]] = []
        documents = query_result['documents'][0]
        metadatas = query_result["metadatas"][0]
        distances = query_result['distances'][0]

        for i in range(0, len(documents)):
            markdown = documents[i]; metadata = metadatas[i]; score = distances[i]
            chunk = Chunk(
                chapter=metadata['chapter'],
                subchapter=metadata['subchapter'],
                markdown=markdown,
                bookname=metadata['bookname'],
            )
            chunks_and_scores.append((chunk, score))

        chunks_and_scores.sort(key=lambda x: x[1]) # sort by most similar text first

        chunks = []
        for chunk, _ in chunks_and_scores: chunks.append(chunk)

        return chunks
