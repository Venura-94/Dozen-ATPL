from dataclasses import dataclass

from src.models.chunk import Chunk


@dataclass
class MCQ:

    id: str

    question: str

    possible_answers: list[str]

    correct_answer_index: int | None = None

    explanations: list[str] | None = None

    sources: list[list[Chunk]] | None = None

    def get_answer_index(self, answer: str) -> int:
        """Enter a string to see if it matches one in the possible answer list.

        Returns:
            int: index of the answer, None if not found
        """
        for i,ans in enumerate(self.possible_answers):
            if answer == ans: return i
        return None