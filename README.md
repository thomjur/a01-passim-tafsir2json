# a01-passim-tafsir2json

This repository includes transformations to create a JSON multiline file for **passim** from a collection of documents (subchapters) from the A01 Tafsir database.

---

## Getting Started

This repository was created using **uv**. To get started, follow these steps:

1.  **Clone the repository**: Download the repository to your local machine using git clone.
2.  **Install uv**: Make sure you have **uv** installed.
3.  **Install dependencies**: Run `uv pip install -r requirements.txt` in the root directory of this repository to set up the local environment.

## Usage

1.  **Prepare your data**: Copy all text documents that need to be converted into the `data` folder. These files are assumed to be from the **Tafsir** database.
2.  **Ensure correct naming**: It is crucial that the filenames for the subchapters follow this specific format:
    `sc.<TAFSIR_ID>_<CHAPTER_ID>_<SUBCHAPTER_ID>.txt`
    For example, a valid filename would be `sc.123_45_67.txt`.
3.  **Run the script**: `uv run main.py`. If the filenames do not conform to this format, the parsing of the **Tafsir ID** and subsequent retrieval of metadata from `tafsir_metadata.csv` will fail.

## Version Information

**1.0.0** - Initial release.
