from src.connectors_old import Connectors
from src.ResultWithSourcesUsed import ResultWithSourcesUsed


def chat_with_data(query: str, conv_history: list[dict] = None) -> tuple[str,list[dict]]:
    """Performs chat with data.

    Args:
        query (str): User query
        conv_history (list[dict], optional): conversation history (role: user/assistant, content). Defaults to None.

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
    Use ONLY the following pieces of retrieved context and provided conversation history to answer
    the question. If you don't know the answer, say that you don't know. 
    Keep the answer concise. The retrieved pieces of context are numbered.
    Question:

    """
    prompt_string += query + '\n'
    prompt_string += 'CONTEXT:  \n'

    for i,doc in enumerate(context_docs):
        prompt_string += f"{i + 1}. {doc.page_content}\n"

    if conv_history:
        prompt_string += "Conversation History: \n"
        for conv in conv_history:
            role = conv["role"]
            if role == 'assistant': role = 'You'
            content = conv["content"]
            prompt_string += f"{role}: {content} \n\n"
    else: prompt_string += "Conversation History: None provided.\n"

    print('PROMPT STRING:')
    print(prompt_string)
    print()
    print()

    result: ResultWithSourcesUsed = structured_llm.invoke(prompt_string)
    sources = []

    # only get the sources that were useful for generating the answer
    for n in result.context_pieces_used:
        index = n-1
        document = context_docs[index]
        sources.append(document.metadata)

    return (result.answer,sources)

