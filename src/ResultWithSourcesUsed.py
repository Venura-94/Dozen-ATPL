from pydantic import BaseModel, Field

class ResultWithSourcesUsed(BaseModel):
    """Pydantic class.
    Used so that llm returns result according to this structure.
    Useful for discarding top k sources that were not required for answer generation.
    """
    answer: str = Field(description='Your answer.')
    context_pieces_used: list[int] = Field(
        description="""An array of the numbers of context pieces used in order of descending importance. For example if you were given
         3 pieces of context and piece 3 was the most important, followed by piece 2 and piece 1 was useless, array must be [3,2] """
    )