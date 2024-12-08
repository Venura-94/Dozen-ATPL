from src import llm_interface as li

class MCQ:
    def __init__(self, question: str, possible_answers: list[str], correct_answer_index: int, id: str = '') -> None:
        self.id = id # just for reference for now
        self.question = question
        self.possible_answers = possible_answers
        self.correct_answer_index = correct_answer_index

        self.explanations: list[str] = [] # holds explanation for each answer (why it's correct or not). In order of self.possible_answers.
        self.sources: list[list[dict]] = [] # holds the sources for each explanation. In order of self.possible_answers.

    def generate_llm_explanations_and_sources(self):
        for possible_answer in self.possible_answers:
            explanation,sources = li.get_explanation_with_sources(
                mcq_question=self.question,
                correct_answer=self.possible_answers[self.correct_answer_index],
                answer_seeking_explanation=possible_answer
            )
            self.explanations.append(explanation)
            self.sources.append(sources)

    def __str__(self) -> str:
        string = 'Question: ' + self.question + '\n'
        string += 'Answers:\n'
        answer_number = 97
        for ans in self.possible_answers:
            string += f'{chr(answer_number)}. {ans}\n'
            answer_number += 1
        string += f'Correct answer: {chr(self.correct_answer_index + 97)}'
        string += '\n'
        string += 'Explanations:\n\n'
        for n,exp in enumerate(self.explanations):
            string += f'{chr(n+97)}. ' + exp + '\n\n'
        string += 'sources:\n\n'
        for m,srcs in enumerate(self.sources):
            string += f'{chr(m+97)}. ' + srcs.__str__() + '\n\n'
        return string
    
    def get_answer_index(self, answer: str) -> int:
        """Enter a string to see if it matches that in the possible answer list.

        Args:
            answer (str): _description_

        Returns:
            int: index of the answer, None if not found
        """
        for i,ans in enumerate(self.possible_answers):
            if answer == ans: return i
        return None
