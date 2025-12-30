from pydantic import BaseModel

class ResultWithSourcesUsed(BaseModel):
    """Pydantic class.
    Used so that llm returns result according to this structure.
    Useful for discarding top k sources that were not required for answer generation.
    """
    answer: str
    context_pieces_used: list[int]