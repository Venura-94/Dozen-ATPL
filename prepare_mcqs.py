# SCRIPT
# Reads the 293 questions from the documents, get the answers from the .csv file, 
# gets explanations and sources for them, and stores as a .pkl file in the extracted_data folder.
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

import json
import time
import io
from dataclasses import asdict

from src.operators.prep_mcqs.mcq_prep import update_MCQs_with_explanations
from src.connectors.storage import LocalStorage
from src.models.mcq import MCQ


# Read the extracted MCQs from storage
mcq_json_bytes = LocalStorage.download_file("mcqs-as-extracted/book8.json")
mcq_json_dicts = json.loads(mcq_json_bytes.decode("utf-8"))
mcqs: list[MCQ] = []
for dict_ in mcq_json_dicts:
    mcqs.append(MCQ(**dict_))

# Use an LLM to generate explanations and stuff
tic = time.time()
update_MCQs_with_explanations(mcqs)
toc = time.time()

# save the MCQs with explanations to storage
mcqs_as_dicts: list[dict] = []
for mcq in mcqs:
    mcqs_as_dicts.append(asdict(mcq))

buffer = io.BytesIO()
buffer.write(json.dumps(mcqs_as_dicts, indent=2).encode("utf-8"))

LocalStorage.upload_file("mcqs-with-explanations/book8.json", buffer.getvalue())

print(f"Took {toc - tic} seconds.")
