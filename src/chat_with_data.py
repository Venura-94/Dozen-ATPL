from pydantic import BaseModel, Field

from src.connectors import Connectors

class ResultWithSourcesUsed(BaseModel):
    answer: str = Field(description='Your answer.')
    context_pieces_used: list[int] = Field(
        description="""An array of the numbers of context pieces used in order of descending importance. For example if you were given
         3 pieces of context and piece 3 was the most important, followed by piece 2 and piece 1 was useless, array must be [3,2] """
    )


def chat_with_data(query: str) -> tuple[str,list[dict]]:
    """Performs chat with data.

    Args:
        query (str): User query

    Returns:
        tuple[str,list[dict]]: answer, sources
    """
    llm = Connectors.get_llm_client()
    structured_llm = llm.with_structured_output(ResultWithSourcesUsed)
    vectorstore = Connectors.get_vectorstore_client()
    retriever = vectorstore.as_retriever()

    context_docs = retriever.invoke(query)

    prompt_string = f"""
    You are an assistant for question-answering tasks. 
    Use ONLY the following pieces of retrieved context to answer
    the question. If you don't know the answer, say that you don't know. 
    Keep the answer concise. The retrieved pieces of context are numbered.
    Question:

    """
    prompt_string += query + '\n'
    prompt_string += 'CONTEXT:  \n'

    for i,doc in enumerate(context_docs):
        prompt_string += f"{i + 1}. {doc.page_content}\n"
    

    result = structured_llm.invoke(prompt_string)
    print(result)
    sources = []

    for n in result.context_pieces_used:
        index = n-1
        document = context_docs[index]
        sources.append(document.metadata)

    return (result.answer,sources)



