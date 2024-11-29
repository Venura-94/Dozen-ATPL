from src.connectors import Connectors

def __generate_keywords_to_fetch_documents(mcq_question: str, correct_answer: str, answer_seeking_explanation: str = None) -> str:
    prompt_string = f"""
    Consider the MCQ Question denoted between triple backticks.
    ```{mcq_question}```
    The correct answer is '{correct_answer}'.
    """

    if (not answer_seeking_explanation) or (answer_seeking_explanation == correct_answer):
        task = f"""
        Your task is to generate text containing keywords to search for appropriate documents from a vectorstore, 
        so that someone else can explain why '{correct_answer}' is the correct answer to this MCQ.
        """
    else:
        task = f"""
        Your task is to generate text containing keywords to search for appropriate documents from a vectorstore, 
        so that someone else can explain why '{answer_seeking_explanation}' is not the correct answer to this MCQ.
        """

    prompt_string += task
    prompt_string += """
    Reply only with the keywords as a string. Don't tell me anything else.
    """

    llm = Connectors.get_llm_client()
    keywords = llm.invoke(prompt_string).content
    print(f'KEYWORDS: {keywords}')
    return keywords

def get_explanation_with_sources(mcq_question: str, correct_answer: str, answer_seeking_explanation: str = None) -> tuple[str,list[dict]]:
    """Performs RAG and gets the explanation of why an MCQ option is incorrect or correct, with sources.

    Returns:
        tuple[str,list[dict]]: explanation, sources
    """
    vectorstore = Connectors.get_vectorstore_client()
    retriever = vectorstore.as_retriever()
    llm = Connectors.get_llm_client()

    keywords = __generate_keywords_to_fetch_documents(mcq_question, correct_answer, answer_seeking_explanation)
    
    context_docs = retriever.invoke(keywords)

    prompt_string = f"""
    Consider the MCQ Question denoted between triple backticks.
    ```{mcq_question}```
    The correct answer is '{correct_answer}'.

    Use ONLY the following pieces of retrieved context to explain why 
    """

    if (not answer_seeking_explanation) or (answer_seeking_explanation == correct_answer):
        task = f"""
        {correct_answer} is the correct answer to this MCQ.
        """
    else:
        task = f"""
        {answer_seeking_explanation} is not the correct answer to this MCQ.
        """

    prompt_string += task
    prompt_string += """If you don't know the answer, say that you don't know.
    You don't need to mention the fact that you used the context in your answer. Keep your answer as short as possible.
    """
    prompt_string += """Context:"""

    sources: list[dict] = []
    for doc in context_docs:
        sources.append(doc.metadata)
        prompt_string += doc.page_content

    explanation = llm.invoke(prompt_string).content

    return (explanation, sources)