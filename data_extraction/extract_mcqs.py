from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv()) # read local .env file

import data_extraction.read_doc as read_doc
from src.MCQ import MCQ
from src import llm_interface as li

def extract_mcqs() -> list[MCQ]:
    """Reads the corrected word document and QnA mapping excel to extract the 293 MCQs from the Revision Questions
    from chapter 18. 

    WARNING: Discard MCQs where answers have not been extracted (len(self.possible_answers) != 4)

    Returns:
        list[MCQ]: _description_
    """
    doc_tree = read_doc.get_document_tree('data/ATPL Ground Training Series - Book 8 Human Performance and Limitations MCQ CORRECTED.docx', ignore_QnA=False)
    ch18 = doc_tree[17]

    # identify the "Revision Questions" part of chapter 18, which contains 293 MCQs
    heading4_items = ch18.get_leaves('Heading 4')
    for item in heading4_items:
        if item.name == 'Revision Questions':
            questions = item

    # extract each MCQ from the 'Revision Questions' section
    mcqs: list[MCQ] = []
    current_question = ''
    current_answers = []
    numbered_list_thats_part_of_the_question_index = 1
    current_level0_list_numId = -1
    mcq_id = 1
    for line in questions.contents:
        if line.list == None: continue
        if line.list[0] == 0: # New MCQ question
            # commit the previous MCQ
            if current_question != '': 
                mcq = MCQ(current_question, current_answers, -1, id=str(mcq_id))
                mcqs.append(mcq)
                mcq_id += 1

            current_answers = []
            current_question = line.name
            numbered_list_thats_part_of_the_question_index = 1
            current_level0_list_numId = line.list[1]
        if line.list[0] == 1 and line.list[1] != current_level0_list_numId: # numbered list that's part of the question
            current_question += '\n' + str(numbered_list_thats_part_of_the_question_index) + '. ' + line.name # a numbered list that's part of the question
            numbered_list_thats_part_of_the_question_index += 1
        if line.list[0] == 1 and line.list[1] == current_level0_list_numId: # answer list
            current_answers.append(line.name)
    if current_question != '': 
        mcq = MCQ(current_question, current_answers, -1, id=str(mcq_id))
        mcqs.append(mcq)
        mcq_id += 1

    
    # map the correct answers
    with open('data/number_letter_mapping.csv','rt') as file: lines = file.readlines()
    for i in range(0,len(lines)):
        line = lines[i]
        correct_ans_letter = line.rsplit(',')[1][0] # [0] to only get the first letter (in case of new line character or a space or something)
        correct_ans_index = ord(correct_ans_letter) - 97
        mcqs[i].correct_answer_index = correct_ans_index


    # print(len(mcqs))
    # for i in range(0,len(mcqs)):
    #     mcq = mcqs[i]
    #     print(i+1)
    #     print(mcq)
    #     print()
    #     print()

    return mcqs

def update_MCQs_with_explanations(mcqs: list[MCQ]):
    """Adds the LLM explanations and sources to the given MCQ objects.
    """
    for mcq in mcqs:
        mcq.generate_llm_explanations_and_sources()
