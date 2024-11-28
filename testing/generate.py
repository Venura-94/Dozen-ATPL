from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field



# prompt_template = ChatPromptTemplate.from_template(template_for_generating_description_search)


class MCQ(BaseModel):
    """_decription_"""

    question: str = Field(description="The question")
    a: str = Field(description='First possible answer (out of four) the user can select')
    b: str = Field(description='Second possible answer (out of four) the user can select')
    c: str = Field(description='Third possible answer (out of four) the user can select')
    d: str = Field(description='Fourth possible answer (out of four) the user can select')
    answer: int = Field(description="The index of the correct answer - 1 if it was the first one, 2 if it was the second one, and so on.")
    explanation: str = Field(description="Explanation of correct answer to the question.")

class MCQs(BaseModel):
    """_decription_"""

    mcqs: list[MCQ] = Field(description="3 possible MCQ objects")

def generate_MCQ_json(input_json: str):
    llm = ChatOpenAI(model="gpt-4o")
    structured_llm = llm.with_structured_output(MCQs)

    template_for_generating_description_search = """8.	Why is it essential to ensure that the combustion heaters are serviceable?
    a.	To prevent carbon dioxide poisoning and possible fire
    b.	To prevent carbon dioxide poisoning, possible fire or explosion
    c.	To prevent carbon monoxide poisoning
    d.	To prevent carbon dioxide poisoning and possible fire
    9.	The effects of smoking, particularly in relation to aviation are:
    a.	an early onset of hypoxia due to an apparent increase in altitude and a degradation of night vision
    b.	an early onset of hypoxia due to an apparent increase in altitude
    c.	an early onset of hypoxia due to an apparent increase in altitude up to a maximum of 40 000 ft
    d.	an early onset of hypoxia due to an apparent increase in altitude with a resulting risk of anaemia
    10.	Will smokers experience hypoxia at a lower or higher cabin altitude than nonsmokers?
    a.	At a higher cabin altitude
    b.	At a lower cabin altitude
    c.	Both will experience hypoxia at approximately the same cabin altitude
    d.	Smoking, although harmful in other ways,  lessens the effects of hypoxia

    Answers: 8c,9a,10b

    Consider the above example of MCQ (each question with 4 possible answers, with only one been correct, and the key provided at the end)

    A chapter from a document in JSON format containing its structure and content is given below denoted between triple backticks. Generate 3 MCQs with keys and explanations using only the data in the json. 

    """

    template_for_generating_description_search += '```'
    template_for_generating_description_search += input_json
    template_for_generating_description_search += '```'

    return structured_llm.invoke(template_for_generating_description_search)



