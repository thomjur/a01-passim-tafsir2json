# a01-passim-tafsir2json

This repository transforms collections of Tafsir (Islamic Qur'anic commentary) text documents from the A01 Tafsir database into JSON Lines format for use with **passim** text reuse detection system.

## Overview

The script processes Arabic text files containing Tafsir subchapters and enriches them with bibliographic metadata (author information, dates, titles) to create a structured JSON Lines output suitable for computational text analysis.

## Prerequisites

- Python 3.12 or higher
- **uv** package manager ([installation guide](https://github.com/astral-sh/uv))

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd a01-passim-tafsir2json
   ```

2. **Install dependencies using uv**:
   ```bash
   uv pip install -r requirements.txt
   ```

## Usage

### 1. Prepare Your Data

Place your Tafsir text files in the `input/` directory. Each file should contain the Arabic text of a single subchapter from a Tafsir work. Note that there is a script `remove_quran_quotes.sh` in the root folder of this repo that deletes all Quranic quotes in the txt files in input/ and stores the cleaned files in a new directory called `no_quranic_quotes/`.

### 2. File Naming Convention

**Critical**: Files must follow this exact naming pattern:
```
sc.<TAFSIR_ID>_<CHAPTER_ID>_<AYA_START>_<AYA_END>.txt
```

**Components**:
- `sc.` - Required prefix
- `<TAFSIR_ID>` - Numeric ID matching an entry in `tafsir-metadata.csv`
- `<CHAPTER_ID>` - Qur'anic chapter (sura) number
- `<AYA_START>_<AYA_END>` - Verse (aya) range

**Example**: `sc.54_37_22_26.txt`
- Tafsir ID: 54 (Adwaʾ al-bayan by al-Shanqiti)
- Chapter: 37 (Surat al-Saffat)
- Verses: 22-26

### 3. Run the Transformation

Basic run (no sura/aya tagging):

```bash
uv run main.py
```

Optionally include series ID, a series description, and Sura and Aya to tag each record (note that Sura and Aya values both must be provided together):

```bash
# long flags
uv run main.py --sura 2 --aya 255 --series-id cluster-q1:6-new --series-description "This cluster includes subchapters commenting on Q1:6 using passim with n=20 and m=3."

# short flags
uv run main.py -s 2 -a 255
```

The script will:
- Process all files in the `input/` directory
- Extract the Tafsir ID from each filename
- Enrich with metadata from `tafsir-metadata.csv`
- Generate a JSON Lines file at `json_output/passim_input.json`

### (Optional:) Statsgen
You can generate an overview of the input files (word/char counts) in `summary.txt` using `./statsgen.sh input/` in the root folder of this project.

## Output Format

Each line in the output JSON contains:
```json
{
  "id": "tafsir.subchapter[UUID]",
  "series": "[UUID]",
  "tafsir_id": "54",
  "tafsir_title": "Adwaʾ al-bayan fi idah al-Qurʾan bi al-Qurʾan",
  "author_name": "Shanqiti, al-",
  "author_death_dce": 1973,
  "author_place_of_death": "Mecca",
  "text": "<Full Arabic text content>"
  "original_text": "<Original text to keep for later>"
  "series_id": "<SERIES-ID> or <EMPTY>",
  "series_description": "<SERIES-DESCRIPTION> or <EMPTY>,
  ["sura"]: 37,
  ["aya"]: 23
}
```

## Tafsir Metadata

The `tafsir-metadata.csv` file contains bibliographic information for each Tafsir work:

| Field | Description |
|-------|-------------|
| `tafsir_id` | Unique numeric identifier |
| `tafsir_title` | Full title of the Tafsir work |
| `author_id` | Unique author identifier |
| `author_name` | Author's name |
| `death_dce` | Death year in DCE (Dionysian Common Era) |
| `place_of_death` | Location where author died |

### Sample Entries

| tafsir_id | tafsir_title | author_name | death_dce | place_of_death |
|-----------|--------------|-------------|-----------|----------------|
| 28 | Irshad al-ʿaql al-salim | Abu al-Suʿud | 1574 | Istanbul |
| 19 | al-Bahr al-muhit | Abu Hayyan | 1345 | Cordoba |
| 52 | Ruh al-maʿani | Alusi, al- | 1854 | Baghdad |

**Note**: Some Tafsir works may have multiple authors. The script handles this by adding numbered fields (e.g., `author_name_2`, `author_death_dce_2`).

## Environment Variables

- `METADATA_PATH`: Custom path to the metadata CSV file (defaults to `tafsir-metadata.csv`)

## Development

### Testing

The project includes comprehensive unit tests for all major functions.

#### Install test dependencies
```bash
uv pip install -e ".[test]"
```

#### Run tests with unittest
```bash
# Run all tests
uv run python -m unittest discover tests

# Run with verbose output
uv run python -m unittest discover tests -v

# Run specific test class
uv run python -m unittest tests.test_main.TestParseTafsirId
```

#### Run tests with pytest (if installed)
```bash
# Run all tests
uv run pytest

# Run with coverage report
uv run pytest --cov=main --cov-report=term-missing

# Run specific test file
uv run pytest tests/test_main.py
```

### Linting and Formatting

```bash
# Check code style
uv run ruff check .

# Format code
uv run ruff format .
```

## Troubleshooting

**Error: "Could not parse Tafsir id"**
- Verify filename follows the exact pattern: `sc.<NUMBER>_<NUMBER>_<NUMBER>_<NUMBER>.txt`
- Ensure the Tafsir ID is numeric

**Error: "Could not retrieve Tafsir name/author"**
- Check that the Tafsir ID in the filename exists in `tafsir-metadata.csv`
- Verify the CSV file is properly formatted

**Empty output file**
- Ensure text files are placed in the `input/` directory
- Check that files contain readable text content

## Version Information

**1.0.4** - Added a delete Quranic quotes script.

**1.0.3** - Added statistic generator (statsgen) script to get an overview of char/word distro between input files.

**1.0.2** - Added a series ID and a series description.

**1.0.1** - Added sura and aya fields (optional). Type hints and docstrings added via Codex CLI.

**1.0.0** - Initial release with core transformation functionality and metadata enrichment
