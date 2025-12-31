from pydantic import BaseModel

class ResultWithSourcesUsed(BaseModel):
    """Pydantic class.
    Used so that llm returns result according to this structure.
    
    The prompt given to the LLM has the retrived context from the vectorstore numbered. So the LLM can tell which numbers actually helped it formulate an answer.
    """
    answer: str
    context_pieces_used: list[int]