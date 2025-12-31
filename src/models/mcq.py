from dataclasses import dataclass

from src.models.chunk import Chunk


@dataclass
class MCQ:

    id: str
    """An ID for the MCQ. e.g. it can be the MCQ question number."""

    question: str

    possible_answers: list[str]

    correct_answer_index: int | None = None

    explanations: list[str] | None = None
    """Explanation for each possible answer explaning why it is wrong or right."""

    sources: list[list[Chunk]] | None = None
    """Corresponding sources for each explanation."""

    def get_answer_index(self, answer: str) -> int:
        """Enter a string to see if it matches one in the possible answer list.

        Returns:
            int: index of the answer, None if not found
        """
        for i,ans in enumerate(self.possible_answers):
            if answer == ans: return i
        return None