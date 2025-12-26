# Streamlit secondary page
# Allows user to chat with the textbook.
# https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps

import streamlit as st
import time

from src import chat_with_data


st.title("Chat with your Textbook 📘")

memory_on = st.toggle("Memory of Conversation History")

def typewriter(text: str):
    """To create typewriter effect in the chat UI
    """
    for char in text:
        yield char
        time.sleep(0.01)


if "messages" not in st.session_state:
    st.session_state.messages = [] # list[dict]
# for conversational memory (will store messages except sources)
if "messages_for_memory" not in st.session_state:
    st.session_state.messages_for_memory = [] # list[dict]

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    if message['role'] != 'source':
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    else:
        source = message["content"]
        with st.chat_message("assistant"):
            with st.popover(f"**Chapter {source['chapter']} -> {source['subchapter']}**"):
                st.markdown(source['markdown'])

# React to user input
if prompt := st.chat_input("Enter question..."): # := operator to assign the user's input to the prompt variable and checked if it's not None in the same line.
    prompt = prompt[:700] # cap length of user query
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    print(f'memory_on: {memory_on}')
    if memory_on: response_string, sources = chat_with_data.chat_with_data(prompt,st.session_state.messages_for_memory)
    else: response_string, sources = chat_with_data.chat_with_data(prompt)
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.write_stream(typewriter(response_string))
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response_string})

    # for conversational memory
    st.session_state.messages_for_memory.append({"role": "user", "content": prompt})
    st.session_state.messages_for_memory.append({"role": "assistant", "content": response_string})
    st.session_state.messages_for_memory = st.session_state.messages_for_memory[-4:] # cap memory

    sources_string = 'Sources:  \n  \n'
    for source in sources:
        source_string = f"Chapter {source['chapter']} -> {source['subchapter']}" + '  \n' # streamlit requires 2 whitespaces in front of the new line for it to work
        with st.chat_message("assistant"):
            with st.popover(f"**Chapter {source['chapter']} -> {source['subchapter']}**"):
                st.markdown(source['markdown'])
        st.session_state.messages.append({"role": "source", "content": source})

    
    # cap to last 18 messages
    st.session_state.messages = st.session_state.messages[-18:]
