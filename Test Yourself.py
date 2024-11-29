# Streamlit Main Page
# Runs the streamlit web app to present to end user
# streamlit run /Users/rehangagamage/Desktop/ATPL/"Test Yourself".py

import random
import streamlit as st
from extracted_data.mcqs_holder import MCQS_Holder

st.set_page_config(
    page_title="Test Yourself",
    page_icon="✍️",
)
st.title('Test Yourself ✍️')
st.sidebar.header('Test Yourself ✍️')

mcqs = MCQS_Holder.get_processed_MCQs()

st.markdown(
    """
    <style>
    .stButton > button {
        text-align: left; /* Align text inside button to the left */
    }
    </style>
    """,
    unsafe_allow_html=True
)

def clear_current_mcq():
    st.session_state.pop('current_mcq')

if st.button('Random MCQ'): clear_current_mcq()

# If there is no currently selected MCQ, pick a random one, else get the currently selected one.
if 'current_mcq' not in st.session_state:
    mcq = random.choice(mcqs)
    st.session_state.current_mcq = mcq
else:
    mcq = st.session_state.current_mcq

st.write(f"**Question:** {mcq.question}")

def check_answer(index):
    if index == mcq.correct_answer_index:
        st.success("Correct! 🎉")
    else:
        st.error("Incorrect. ❌")
    explanation: str = mcq.explanations[index]
    explanation = explanation.replace('\n','  \n') # streamlit requires 2 whitespaces in front of the new line for it to work
    st.info(explanation)
    sources = mcq.sources[i]
    sources_string = ''
    for source in sources:
        sources_string += f"Chapter {source['chapter']} -> {source['subchapter']}" + '  \n' # streamlit requires 2 whitespaces in front of the new line for it to work
    st.warning(sources_string)


# Display options as buttons
for i,option in enumerate(mcq.possible_answers):
    if st.button(option, key=i):
        check_answer(i)