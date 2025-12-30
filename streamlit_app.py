import streamlit as st

# Define the pages
page_1 = st.Page("streamlit_pages/chat_with_textbook.py", title="Chat with your Textbook (Beta)", icon="📘")
page_2 = st.Page("streamlit_pages/paginated_mcqs.py", title="Paginated MCQs", icon="📋")
page_3 = st.Page("streamlit_pages/random_mcq.py", title="Random MCQ", icon="🎲")

# Set up navigation
pg = st.navigation([page_1, page_2, page_3])

# Run the selected page
pg.run()