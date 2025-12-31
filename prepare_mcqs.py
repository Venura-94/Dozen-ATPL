# Script to read extracted MCQs from the storage solution, have an LLM generate explanations for them
# and then save them back to the storage solution for use by our app

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

import json
import time
import io
from dataclasses import asdict

from src.operators.prep_mcqs.mcq_prep import update_MCQs_with_explanations
from src.connectors.storage import LocalStorage
from src.models.mcq import MCQ


BOOK_NAME = "book8"

# Read the extracted MCQs from storage
mcq_json_bytes = LocalStorage.download_file(f"mcqs-as-extracted/{BOOK_NAME}.json")
mcq_json_dicts = json.loads(mcq_json_bytes.decode("utf-8"))
mcqs: list[MCQ] = []
for dict_ in mcq_json_dicts:
    mcqs.append(MCQ(**dict_))

# mcqs = mcqs[:3] # remove after testing

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

LocalStorage.upload_file(f"mcqs-with-explanations/{BOOK_NAME}.json", buffer.getvalue())

print(f"Took {toc - tic} seconds.")
