from src.connectors.llm import LLM
from src.models.result_with_sources_used import ResultWithSourcesUsed
from src.models.chunk import Chunk
from src.models.mcq import MCQ
from src.connectors.embeddings import Embeddings
from src.connectors.vectorstore import ChromaLocal
from src import config


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

    llm = LLM.get_openai_client()
    response = llm.responses.create(
        input=prompt_string,
        model=config.LLM_MODEL
    )
    keywords = response.output_text
    print(f'KEYWORDS: {keywords}')
    return keywords


def __get_explanation_with_sources(mcq_question: str, correct_answer: str, answer_seeking_explanation: str = None) -> tuple[str,list[Chunk]]:
    """Performs RAG and gets the explanation of why an MCQ option is incorrect or correct, with sources.

    Returns:
        tuple[str,list[dict]]: explanation, sources
    """

    keywords = __generate_keywords_to_fetch_documents(mcq_question, correct_answer, answer_seeking_explanation)

    query_embedding = Embeddings.embed_texts([keywords])[0]
    context = ChromaLocal.query_collection("book8", query_embedding)
    
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
    The retrieved pieces of context are numbered.
    """
    prompt_string += 'CONTEXT:  \n'
    for i, chunk in enumerate(context):
        prompt_string += f"{i + 1}. {chunk.markdown}\n"

    sources: list[dict] = []
    llm_client = LLM.get_openai_client()
    response = llm_client.responses.parse(
        model=config.LLM_MODEL,
        input=prompt_string,
        text_format=ResultWithSourcesUsed,
    )
    result = response.output_parsed
    print(result)

    # only get the sources that were useful for generating the answer
    for n in result.context_pieces_used:
        index = n-1
        chunk = context[index]
        sources.append(chunk)

    return (result.answer, sources)

def generate_llm_explanations_and_sources(mcq: MCQ):
    mcq.explanations = []; mcq.sources = []

    for possible_answer in mcq.possible_answers:
        explanation, sources = __get_explanation_with_sources(
            mcq_question=mcq.question,
            correct_answer=mcq.possible_answers[mcq.correct_answer_index],
            answer_seeking_explanation=possible_answer
        )
        mcq.explanations.append(explanation)
        mcq.sources.append(sources)