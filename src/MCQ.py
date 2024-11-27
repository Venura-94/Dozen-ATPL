from src import llm_interface as li

class MCQ:
    def __init__(self, question: str, possible_answers: list[str], correct_answer_index: int, id: str = '') -> None:
        self.id = id
        self.question = question
        self.possible_answers = possible_answers
        self.correct_answer_index = correct_answer_index

        self.explanations: list[str] = [] # holds explanation for each answer (why it's correct or not)
        for _ in range(0,len(possible_answers)): self.explanations.append('')
        self.sources: list[list[dict]] = [] # holds the sources for each explanation.

    def generate_llm_explanations_and_sources(self):
        for possible_answer in self.possible_answers:
            explanation,sources = li.get_explanation_with_sources(
                mcq_question=self.question,
                correct_answer=self.possible_answers[self.correct_answer_index],
                answer_seeking_explanation=possible_answer
            )
            self.explanations.append(explanation)
            self.sources.append(sources)
