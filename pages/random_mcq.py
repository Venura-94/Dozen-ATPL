# Streamlit Main Page
# Runs the streamlit web app to present to end user
# streamlit run /Users/rehangagamage/Desktop/ATPL/"Random MCQ".py

import random
import streamlit as st
from extracted_data.mcqs_holder import MCQS_Holder


st.title('Random MCQ 🎲')

# Get mcqs
mcqs = MCQS_Holder.get_processed_MCQs()

# Hack to left-align buttons
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

# Random MCQ button
def clear_current_mcq():
    st.session_state.pop('current_mcq')
if st.button('Random MCQ'): clear_current_mcq()

# If there is no currently selected MCQ, pick a random one, else get the currently selected one. (session state)
if 'current_mcq' not in st.session_state:
    mcq = random.choice(mcqs)
    st.session_state.current_mcq = mcq
else:
    mcq = st.session_state.current_mcq

# Present MCQ on screen
## Write the question
st.write(f"**Question:** {mcq.question}")

def check_answer(index):
    """Checks if the button user has selected for the question is correct or wrong and generates feedback.
    """
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

# Present MCQ on screen
## Display options as buttons
for i,option in enumerate(mcq.possible_answers):
    if st.button(option, key=i):
        check_answer(i)