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

Place your Tafsir text files in the `data/` directory. Each file should contain the Arabic text of a single subchapter from a Tafsir work.

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

```bash
uv run main.py
```

The script will:
- Process all files in the `data/` directory
- Extract the Tafsir ID from each filename
- Enrich with metadata from `tafsir-metadata.csv`
- Generate a JSON Lines file at `json/passim_input.json`

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
  "text": "[Full Arabic text content]"
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
- Ensure text files are placed in the `data/` directory
- Check that files contain readable text content

## Version Information

**1.0.0** - Initial release with core transformation functionality and metadata enrichment
