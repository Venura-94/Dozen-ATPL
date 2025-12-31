from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

import io
import json
from dataclasses import asdict

from src.operators.prep_mcqs.mcq_prep import extract_mcqs
from src.connectors.storage import LocalStorage


mcqs = extract_mcqs("textbook_input/ATPL Ground Training Series - Book 8 Human Performance and Limitations MCQ CORRECTED.docx", "textbook_input/number_letter_mapping.csv")
mcqs_as_dicts: list[dict] = []
for mcq in mcqs:
    mcqs_as_dicts.append(asdict(mcq))

buffer = io.BytesIO()
buffer.write(json.dumps(mcqs_as_dicts, indent=2).encode("utf-8"))

LocalStorage.upload_file("mcqs-as-extracted/book8.json", buffer.getvalue())