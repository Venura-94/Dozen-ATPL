from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

from src.connectors import Connectors


def chat_with_data(query: str) -> tuple[str,list[dict]]:
    """Performs chat with data.

    Args:
        query (str): User query

    Returns:
        tuple[str,list[dict]]: answer, sources
    """
    llm = Connectors.get_llm_client()
    vectorstore = Connectors.get_vectorstore_client()
    retriever = vectorstore.as_retriever()

    system_prompt = (
        "You are an assistant for question-answering tasks. "
        "Use ONLY the following pieces of retrieved context to answer "
        "the question. If you don't know the answer, say that you "
        "don't know. Keep the "
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

    result = rag_chain.invoke({"input": query})

    answer = result['answer']
    sources = []

    context_documents = result['context']
    for document in context_documents:
        sources.append(document.metadata)

    return (answer,sources)



