import os
import io
import uuid
import json
import pandas as pd
import logging
from dotenv import load_dotenv

load_dotenv()

DATA_PATH = "data/"
OUTPUT_PATH = "json/"
METADATA_PATH = os.getenv("METADATA_PATH", "tafsir-metadata.csv")
OUTPUT_FILE_PATH = os.path.join(OUTPUT_PATH, "passim_input.json")
METADATA_EXISTS = True if os.path.exists(METADATA_PATH) else False
logging.basicConfig(level=logging.DEBUG)

# Empty output folder
if os.path.exists(OUTPUT_FILE_PATH):
    os.remove(OUTPUT_FILE_PATH)

# Load metadata if exists
if METADATA_EXISTS:
    print("Loading metadata...")
    df_metadata = pd.read_csv(METADATA_PATH)
else:
    print(f"{METADATA_PATH} file could not be found...")


def main():
    for f in os.listdir(DATA_PATH):
        with open(os.path.join(DATA_PATH, f), "r") as file:
            create_json(file)


def add_metadata(input_dict: dict, filename: str):
    '''Helper function to add metadata from tafsir-metadata.csv
    to the JSON file'''
    # Get the tafsir id
    tafsir_id = parse_tafsir_id(filename)
    if tafsir_id == "":
        print("Could not parse Tafsir id... aborting metadata retrieval.")
        return
    input_dict["tafsir_id"] = tafsir_id
    # Get Tafsir title
    df_selection = df_metadata.loc[df_metadata["tafsir_id"] == int(tafsir_id), ["tafsir_title"]].reset_index()
    if df_selection.empty:
        print("Could not retrieve Tafsir name")
    else:
        input_dict["tafsir_title"] = df_selection.at[0, "tafsir_title"]

    # Get author name
    df_selection = df_metadata.loc[df_metadata["tafsir_id"] == int(tafsir_id), ["author_name"]].reset_index()
    if df_selection.empty:
        print("Could not retrieve author name")
    elif len(df_selection) > 1:  # There might be multiple authors
        for idx, _ in df_selection.iterrows():
            if idx == 0:
                input_dict["author_name"] = df_selection.at[0, "author_name"]
            else:
                input_dict[f"author_name_{idx+1}"] = df_selection.at[idx, "author_name"]
    else:
        input_dict["author_name"] = df_selection.at[0, "author_name"]

    # Get author death date (dce)
    df_selection = df_metadata.loc[df_metadata["tafsir_id"] == int(tafsir_id), ["death_dce"]].reset_index()
    if df_selection.empty:
        print("Could not retrieve author death date")
    elif len(df_selection) > 1:  # There might be multiple authors
        for idx, _ in df_selection.iterrows():
            if idx == 0:
                input_dict["author_death_dce"] = int(df_selection.at[0, "death_dce"])
            else:
                input_dict[f"author_death_dce_{idx+1}"] = int(df_selection.at[idx, "death_dce"])
    else:
        input_dict["author_death_dce"] = int(df_selection.at[0, "death_dce"])

    # Get author place of death
    df_selection = df_metadata.loc[df_metadata["tafsir_id"] == int(tafsir_id), ["place_of_death"]].reset_index()
    if df_selection.empty:
        print("Could not retrieve author place of death")
    elif len(df_selection) > 1:  # There might be multiple authors
        for idx, _ in df_selection.iterrows():
            if idx == 0:
                input_dict["author_place_of_death"] = df_selection.at[0, "place_of_death"] if not pd.isna(df_selection.at[0, "place_of_death"]) else ""
            else:
                input_dict[f"author_place_of_death_{idx+1}"] = df_selection.at[idx, "place_of_death"] if not pd.isna(df_selection.at[idx, "place_of_death"]) else ""
    else:
        input_dict["author_place_of_death"] = df_selection.at[0, "place_of_death"] if not pd.isna(df_selection.at[0, "place_of_death"]) else ""


def parse_tafsir_id(filename: str) -> str:
    '''Helper function to parse tafsir id from document strings like
    sc.1_34_44_46.txt (sc.<TAFSIR_ID>_<CHAPTER_ID>_<AYA_RANGE>)'''
    parts = filename.split("_")
    if len(parts) != 4:
        return ""
    parts = parts[0].split(".")
    if len(parts) != 2:
        return ""
    if not parts[1].isdigit():
        return ""
    return parts[1]


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

    # Add metadata if possible
    if METADATA_EXISTS:
        add_metadata(json_dict, file.name)

    # We copy the entire text from the file into the "text" field
    # We also create a second column to keep the full text as 
    # separate field for later, since passim might only keep
    # certain parts of the text
    json_dict["text"] = file.read()
    json_dict["original_text"] = json_dict["text"]

    # We dump the dict into the output folder
    with open(OUTPUT_FILE_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(json_dict) + "\n")


if __name__ == "__main__":
    main()
