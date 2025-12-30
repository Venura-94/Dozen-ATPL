import json

from src.models.mcq import MCQ
from src.connectors.storage import LocalStorage


class MCQ_Holder:
    """Singleton class to hold the processed MCQs, to avoid reading it from disk all the time.
    """

    __mcqs: list[MCQ] = None

    @classmethod
    def get_processed_MCQs(cls, filepath: str) -> list[MCQ]:
        """Returns the processed MCQs from the singleton holder (to avoid reading from disk all the time).
        Discards MCQs that don't have 4 answers.
        """
        if cls.__mcqs == None:
            print(f'Loading MCQs from {filepath}')
            mcq_json_bytes = LocalStorage.download_file(filepath)
            mcq_json_dicts = json.loads(mcq_json_bytes.decode("utf-8"))
            mcqs: list[MCQ] = []
            for dict_ in mcq_json_dicts:
                mcqs.append(MCQ(**dict_))

            cls.__mcqs = mcqs

            for i,mcq in enumerate(cls.__mcqs):
                if len(mcq.possible_answers) != 4: 
                    cls.__mcqs.remove(mcq)
                    print(f'Removed MCQ {i+1}')
        return cls.__mcqs