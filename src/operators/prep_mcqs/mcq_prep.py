from src.operators.read_word_doc import get_document_tree
from src.models.mcq import MCQ
from src.operators.prep_mcqs.llm_helper import generate_llm_explanations_and_sources


def extract_mcqs(docx_filepath: str, mcq_answers_csv_filepath: str) -> list[MCQ]:
    """Reads the corrected word document and QnA mapping excel to extract the 293 MCQs from the Revision Questions
    from chapter 18. 

    Returns:
        list[MCQ]: _description_
    """
    doc_tree = get_document_tree(docx_filepath, ignore_QnA=False)
    ch18 = doc_tree[17]

    # identify the "Revision Questions" part of chapter 18, which contains 293 MCQs
    heading4_items = ch18.get_leaves('Heading 4')
    for item in heading4_items:
        if item.text_content == 'Revision Questions':
            questions = item

    # extract each MCQ from the 'Revision Questions' section
    mcqs: list[MCQ] = []
    current_question = ''
    current_answers = []
    numbered_list_thats_part_of_the_question_index = 1
    current_level0_list_numId = -1
    mcq_id = 1
    for line in questions.child_blocks:
        if line.list_positioning == None: continue
        if line.list_positioning[0] == 0: # New MCQ question
            # commit the previous MCQ
            if current_question != '': 
                mcq = MCQ(str(mcq_id), current_question, current_answers)
                mcqs.append(mcq)
                mcq_id += 1

            current_answers = []
            current_question = line.text_content
            numbered_list_thats_part_of_the_question_index = 1
            current_level0_list_numId = line.list_positioning[1]
        if line.list_positioning[0] == 1 and line.list_positioning[1] != current_level0_list_numId: # numbered list that's part of the question
            current_question += '\n' + str(numbered_list_thats_part_of_the_question_index) + '. ' + line.text_content # a numbered list that's part of the question
            numbered_list_thats_part_of_the_question_index += 1
        if line.list_positioning[0] == 1 and line.list_positioning[1] == current_level0_list_numId: # answer list
            current_answers.append(line.text_content)
    if current_question != '': 
        mcq = MCQ(str(mcq_id), current_question, current_answers)
        mcqs.append(mcq)
        mcq_id += 1

    
    # map the correct answers
    with open(mcq_answers_csv_filepath,'rt') as file: lines = file.readlines()
    for i in range(0,len(lines)):
        line = lines[i]
        correct_ans_letter = line.rsplit(',')[1][0] # [0] to only get the first letter (in case of new line character or a space or something)
        correct_ans_index = ord(correct_ans_letter) - 97
        mcqs[i].correct_answer_index = correct_ans_index

    return mcqs

def update_MCQs_with_explanations(mcqs: list[MCQ]):
    """Adds the LLM explanations and sources to the given MCQ objects.
    """
    for i,mcq in enumerate(mcqs):
        print(f'MCQ {i+1}')
        try: generate_llm_explanations_and_sources(mcq)
        except IndexError: continue
