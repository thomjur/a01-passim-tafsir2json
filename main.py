import os
import io
import uuid
import json

DATA_PATH = "data/"
OUTPUT_PATH = "json/"
OUTPUT_FILE_PATH = os.path.join(OUTPUT_PATH, "passim_input.json")

# Empty output folder
if os.path.exists(OUTPUT_FILE_PATH):
    os.remove(OUTPUT_FILE_PATH)

def main():
    for f in os.listdir(DATA_PATH):
        with open(os.path.join(DATA_PATH, f), "r") as file:
            create_json(file)


def create_json(file: io.TextIOWrapper):
    '''Creating a JSON object for passim.'''
    json_dict = {}
    # Creating a unique id
    _unique_uuid = str(uuid.uuid4())
    _id = "tafsir.subchapter" + _unique_uuid
    # Since we also want to have unique series for each subchapter, we use
    # parts of the document id for the series
    _series = _unique_uuid

    json_dict["id"] = _id
    json_dict["series"] = _series

    # We copy the entire text from the file into the "text" field
    json_dict["text"] = file.read()

    # We dump the dict into the output folder
    with open(OUTPUT_FILE_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(json_dict) + "\n")


if __name__ == "__main__":
    main()
