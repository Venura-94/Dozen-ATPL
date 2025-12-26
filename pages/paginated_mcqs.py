# Streamlit secondary page
# Paginated MCQs.

import streamlit as st
import math

from extracted_data.mcqs_holder import MCQS_Holder
from src.MCQ import MCQ

MCQS_PER_PAGE = 10


st.title('Paginated MCQs 📋')

# Get mcqs
all_mcqs = MCQS_Holder.get_processed_MCQs()

# Initialize session state if required
if 'page_number' not in st.session_state:
    st.session_state.page_number = 1
    st.session_state.user_answers = {}
    

# Paginate MCQs
## Enable/disable navigation buttons depending on page number
if st.session_state.page_number == 1: prev_button_disabled = True
else: prev_button_disabled = False
if st.session_state.page_number >= len(all_mcqs)/MCQS_PER_PAGE: next_button_disabled = True
else: next_button_disabled = False
## Create navigation
prev_page_col, page_number_col, next_page_col = st.sidebar.columns(3)
def go_to_previous_page(): st.session_state.page_number -= 1 # add checks in production deployment
def go_to_next_page(): st.session_state.page_number += 1 # add checks in production deployment
prev_page_col.button('◀️',on_click=go_to_previous_page, disabled=prev_button_disabled)
next_page_col.button('▶️', on_click=go_to_next_page, disabled=next_button_disabled)
## Select the MCQ slice to display based on page number and MCQS_PER_PAGE
start_index = (st.session_state.page_number - 1) * MCQS_PER_PAGE
end_index = start_index + MCQS_PER_PAGE
mcqs = all_mcqs[start_index:end_index]
page_number_col.write(f'{st.session_state.page_number} / {math.ceil(len(all_mcqs)/MCQS_PER_PAGE)}')
go_to_page_label_col, enter_page_number_col = st.sidebar.columns(2)
go_to_page_label_col.write('Go to page')
def user_manually_enters_page():
    user_desired_page_number = st.session_state['user_manually_entered_page']
    st.session_state.page_number = user_desired_page_number
user_desired_page_number = enter_page_number_col.number_input(
    label='Go to page', value=st.session_state.page_number, label_visibility='collapsed', key='user_manually_entered_page',
    on_change=user_manually_enters_page
    )

def check_answer(index: int, column, mcq: MCQ):
    """Checks if the given index matches the correct answer or not of the MCQ,
    and generates feedback in the given column.

    Args:
        index (int): Index of the answer user has chosen
        column (_type_): Usually we expect the right column here, since we usually want the feedback to be generated on the right of the MCQ
        mcq (MCQ): _description_
    """
    if index == mcq.correct_answer_index:
        column.success("Correct! 🎉")
        st.session_state.user_answers[mcq.id][1] = True
    else:
        column.error("Incorrect. ❌")
        st.session_state.user_answers[mcq.id][1] = False
    explanation: str = mcq.explanations[index]
    explanation = explanation.replace('\n','  \n') # streamlit requires 2 whitespaces in front of the new line for it to work
    column.info(explanation)
    sources = mcq.sources[index]
    sources_string = ''
    for source in sources:
        sources_string += f"Chapter {source['chapter']} -> {source['subchapter']}" + '  \n' # streamlit requires 2 whitespaces in front of the new line for it to work
    column.warning(sources_string)

def radio_callback(mcq_id):
    """Used to update session state with user progress once they click an MCQ answer.

    Args:
        mcq_id (_type_): MCQ ID is used to identify which radio selection was used.
    """
    selection = st.session_state[mcq_id]
    index = mcq.get_answer_index(selection)
    st.session_state.user_answers[mcq_id] = [index, None]

# Display MCQs as streamlit radio
for mcq in mcqs:
    left, right = st.columns(2)
    pre_selection = None
    if mcq.id in st.session_state.user_answers:
        pre_selection = st.session_state.user_answers[mcq.id][0]
    selection = left.radio(
        label=f"**{mcq.id}:**  {mcq.question}",
        options=mcq.possible_answers,
        index=pre_selection,
        key=mcq.id,
        on_change=radio_callback,
        args=(mcq.id,)
    )
    if selection != None:
        index = mcq.get_answer_index(selection)
        st.session_state.user_answers[mcq.id] = [index, None] # Didn't spend time wrapping my head around this, but this line must be here, despite been present in the radio on_click callback, otherwise it won't persist when switching between pages
        check_answer(index, right, mcq)
    st.divider()

# Update progress in the sidebar
st.sidebar.divider()
st.sidebar.title('**Progress**')
correct_count = 0
for value in st.session_state.user_answers.values():
    if value[1] == True: correct_count += 1
done_count = len(st.session_state.user_answers)
remaining_count = len(all_mcqs) - done_count
st.sidebar.write(f'Correct: {correct_count}')
st.sidebar.write(f'Incorrect: {done_count-correct_count}')
st.sidebar.write(f'Remaining: {remaining_count}')