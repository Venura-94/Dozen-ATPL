# Streamlit secondary page
# Allows user to chat with the textbook.
# https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps

import streamlit as st
import time

from src import chat_with_data

st.set_page_config(
    page_title="Chat with your Textbook",
    page_icon="📘",
)
st.title("Chat with your Textbook 📘")
st.sidebar.header('Chat with your Textbook 📘')

def typewriter(text: str):
    """To create typewriter effect in the chat UI
    """
    for char in text:
        yield char
        time.sleep(0.01)


if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Enter question..."): # := operator to assign the user's input to the prompt variable and checked if it's not None in the same line.
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})


    response_string, sources = chat_with_data.chat_with_data(prompt)
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.write_stream(typewriter(response_string))
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response_string})
    sources_string = 'Sources:  \n  \n'
    for source in sources:
        sources_string += f"Chapter {source['chapter']} -> {source['subchapter']}" + '  \n' # streamlit requires 2 whitespaces in front of the new line for it to work
    with st.chat_message("assistant"):
        st.write_stream(typewriter(sources_string))
    st.session_state.messages.append({"role": "assistant", "content": sources_string})

    
    # cap to last 18 messages
    st.session_state.messages = st.session_state.messages[-18:]
