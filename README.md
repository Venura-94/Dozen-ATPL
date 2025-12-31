# Intro
This project is an exam assistant for the **Airline Transport Pilot Licence (ATPL)**.

The ATPL syllabus includes a few textbooks. Each textbook is divided into chapters, which themselves are divided into subchapters. The final chapter of the textbook is a specimen MCQ paper.

Our system ingests the textbook and chunks it into subchapter chunks and stores them in a vectorstore (the speciment paper chapter is ignored, so are the sample MCQs at the end of each chapter).

We then allow a chat with your textbook RAG function. The chatbot gives sources for each answer, referencing the subchapter level chunks.

Additionally we can also ingest the end-of-textbook MCQs with the answer sheet. An LLM is then used to generate explanations of why each answer is correct or wrong, with sources to the knowledge base provided.

This is used to provide an interface where the student can undertake MCQ questions and get instant feedback.

## Demo Videos
https://drive.google.com/drive/folders/1jaHJvZA_qw2BP9Lhc6MWXzlmF5x-xYXA?usp=drive_link

# Setup

## Environmental Variables
- OPENAI_API_KEY

## Python packages
Install the packages in `requirements.txt`.

# Usage

## Launching Streamlit Web UI
```bash
streamlit run streamlit_app.py
```
### Streamlit UI Demo Videos
https://drive.google.com/drive/folders/1jaHJvZA_qw2BP9Lhc6MWXzlmF5x-xYXA?usp=drive_link

## Ingesting Textbook Knowledge
### Prepare the Textbook
1. The PDF textbook must be converted to word. (Use of Word 365 recommended).
1. Make a copy of the word document.
1. Remove the MCQ sections from this copy.
1. Use MS Word Styles to ensure that:
    1. chapter headings are at Heading level 2
    1. subchapter headings are at Heading level 3
    1. appropriate subheadings under subchapters are at Heading level 4
    1. all other parts are styled at Normal level
### Run the ingestion script
Edit the `FILENAME` and `BOOK_NAME` constants in the script.
```bash
python3 ingest_textbook.py
```
This will output artifacts to `textbook_tree/` and `textbook_chunks/` folders as json files for visualization. The vectorstore will be created.

## Extraction, Preparation and Ingestion of MCQs with Explanations
1. The PDF textbook must be converted to word. (Use of Word 365 recommended).
1. Make a copy of the word document.
1. Keep only the specimen paper chapter.
1. TODO: add the remaining instructions on how to format the word doc
1. Run `extract_mcqs.py` (change the filepaths accordingly). The extracted MCQs will be saved to storage as a json.
    1. If required, this json file can be edited.
1. Prepare MCQ number to correct answer map as a .csv file (see `textbook_input/number_letter_mapping.csv` for an example)
1. Run `prepare_mcqs.py` (change the book name constant in the script). This will prepare the MCQs with LLM generated explanations and make them available for the streamlit app.

> [!WARNING]
> - MCQ identification heavily depends on the .docx list and nested list structures used.
> - You may have to edit the word document if lists have been skewed during the PDF -> Word conversion.
> - Double-clicking a list number shows its parallel lists. Sometimes the 'copy formating' function may work.
> - Worst case, you may have to type the skewed MCQ question, or edit the extracted json file in storage.

