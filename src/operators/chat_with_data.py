from src.models.result_with_sources_used import ResultWithSourcesUsed
from src.connectors.llm import LLM
from src.connectors.vectorstore import ChromaLocal
from src.connectors.embeddings import Embeddings
from src.models.chunk import Chunk
from src import config


def __formulate_instruction(context: list[Chunk], user_query: str) -> str:
    instruction = f"""
    You are an assistant for question-answering tasks. 
    Use ONLY the following pieces of retrieved context and provided conversation history to answer
    the question. If you don't know the answer, say that you don't know. 
    Keep the answer concise. The retrieved pieces of context are numbered.
    Question:

    """
    instruction += user_query + '\n'
    instruction += 'CONTEXT:  \n'

    for i, chunk in enumerate(context):
        instruction += f"{i + 1}. {chunk.markdown}\n"

    return instruction


def chat_with_data(query: str, conv_history: list[dict] = None) -> tuple[str,list[Chunk]]:
    
    # perform retrieval from the vectorstore
    query_embedding = Embeddings.embed_texts([query])[0]
    context = ChromaLocal.query_collection("book8", query_embedding)

    instruction = __formulate_instruction(context, query)
    
    llm_client = LLM.get_openai_client()

    messages = []

    if conv_history:
        for conv in conv_history:
            if conv['role'].lower().strip() == 'system': continue # safety check
            messages.append({
                "role": conv['role'],
                "content": conv["content"]
            })

    messages.append({
        "role": "system",
        "content": instruction,
    })


    response = llm_client.responses.parse(
        model=config.LLM_MODEL,
        input=messages,
        text_format=ResultWithSourcesUsed,
    )

    result = response.output_parsed

    # get the sources that, according to the LLM, were useful for generating the answer
    sources = []
    for n in result.context_pieces_used:
        index = n-1
        chunk = context[index]
        sources.append(chunk)

    return (result.answer,sources)

