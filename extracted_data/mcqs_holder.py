import pickle

from src.MCQ import MCQ

class MCQS_Holder:
    """Singleton class to hold the processed MCQs, to avoid reading it from disk all the time.
    """

    __mcqs: list[MCQ] = None

    @classmethod
    def get_processed_MCQs(cls) -> list[MCQ]:
        """Returns the processed MCQs from the singleton holder (to avoid reading from disk all the time).
        Discards MCQs that don't have 4 answers.
        """
        if cls.__mcqs == None:
            print('Reading MCQs pickle file')
            with open('extracted_data/mcqs.pkl','rb') as file:
                cls.__mcqs: list[MCQ] = pickle.load(file)
            for i,mcq in enumerate(cls.__mcqs):
                if len(mcq.possible_answers) != 4: cls.__mcqs.remove(mcq)
                print(f'Removed MCQ {i+1}')
        return cls.__mcqs