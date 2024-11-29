from src.connectors import Connectors
from src.ResultWithSourcesUsed import ResultWithSourcesUsed


def chat_with_data(query: str) -> tuple[str,list[dict]]:
    """Performs chat with data.

    Args:
        query (str): User query

    Returns:
        tuple[str,list[dict]]: answer, sources
    """
    llm = Connectors.get_llm_client()
    structured_llm = llm.with_structured_output(ResultWithSourcesUsed) # This setup means that llm returns the answer with useless sources dropped from the top k context documents.
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
    

    result: ResultWithSourcesUsed = structured_llm.invoke(prompt_string)
    print(result)
    sources = []

    # only get the sources that were useful for generating the answer
    for n in result.context_pieces_used:
        index = n-1
        document = context_docs[index]
        sources.append(document.metadata)

    return (result.answer,sources)



