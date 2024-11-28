#### Environmental Variables
- OPENAI_API_KEY - for generation
- AZURE_OPENAI_EMBEDDINGS_ENDPOINT - for embeddings
- AZURE_OPENAI_API_KEY - for embeddings
- AZURE_OPENAI_EMBEDDINGS_API_VERSION - for embeddings

#### Main Programs (in execution order)
- create_vs.py - Reads the word document (python-docx) and ingests knowledge (Chapter 2 - 17 inclusive, ignores questions and answers), and creates vectorstore.
- prepare_mcqs.py - Reads the 293 questions from the documents, get the answers from the .csv file, gets explanations and sources for them, and stores as a .pkl file in the extracted_data folder.
- present_mcqs.py - Runs the streamlit web app to present to end user

#### Prerequisites
ATPL PDF must be converted to a word document using Word 365 (requires internet connection).
This identifies Chapters as 'Heading 2' blocks, and sub-chapters as 'Heading 3' blocks, which we need to quantize the structure of the document.
Regarding the 293 MCQ question in chapter 18:
- MCQ identification heavily depends on the .docx list and nested list structures used.
- You may have to edit the word document if lists have been skewed during the PDF -> Word conversion.
- Double-clicking a list number shows its parallel lists. Sometimes the 'copy formating' function may work.
- Worst case, you may have to type the skewed MCQ question.

