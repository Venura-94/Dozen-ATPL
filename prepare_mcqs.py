# SCRIPT
# Reads the 293 questions from the documents, get the answers from the .csv file, 
# gets explanations and sources for them, and stores as a .pkl file in the extracted_data folder.

import pickle

from data_extraction import extract_mcqs

mcqs = extract_mcqs.extract_mcqs()
extract_mcqs.update_MCQs_with_explanations(mcqs)

for i in range(0,len(mcqs)):
    mcq = mcqs[i]
    print(i+1)
    print(mcq)
    print()
    print()

with open('extracted_data/mcqs.pkl','wb') as file:
    pickle.dump(mcqs, file)






# import src.llm_interface as li

# ans,sources = li.get_explanation_with_sources(
#     mcq_question='An individual who has consumed a moderate amount of alcohol prior to sleep is likely to have:',
#     correct_answer='less REM sleep',
#     answer_seeking_explanation='a longer sleep'
# )

# print('ANSWER:')
# print(ans)
# print('SOURCES:')
# for source in sources:
#     print(source)
