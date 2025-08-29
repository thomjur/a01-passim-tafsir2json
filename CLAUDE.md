# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repository transforms collections of Tafsir (Islamic Qur'anic commentary) text documents into JSON format for use with the passim text reuse detection system. The project processes Arabic text files from the A01 Tafsir database and enriches them with metadata.

## Development Commands

### Running the main script
```bash
uv run main.py
```

### Testing
```bash
# Run all unit tests
uv run python -m unittest discover tests -v

# Install test dependencies for pytest
uv pip install -e ".[test]"

# Run with pytest and coverage (if installed)
uv run pytest --cov=main --cov-report=term-missing
```

### Linting
```bash
uv run ruff check .
uv run ruff format .
```

### Installing dependencies
```bash
uv pip install -r requirements.txt
```

## Architecture

### Data Flow
1. **Input**: Text files in `data/` directory following the naming convention `sc.<TAFSIR_ID>_<CHAPTER_ID>_<AYA_RANGE>.txt`
2. **Metadata Enrichment**: The script reads `tafsir-metadata.csv` to add author and publication information
3. **Output**: Single JSON lines file at `json/passim_input.json` where each line is a complete JSON document

### Key Components

- **main.py**: Core transformation logic that:
  - Iterates through all files in the `data/` directory
  - Parses the tafsir ID from filenames using the `parse_tafsir_id()` function
  - Enriches each document with metadata from the CSV file (tafsir title, author name, death date, place of death)
  - Generates unique UUIDs for document identification
  - Outputs JSON lines format suitable for passim

### Critical Requirements

- **Filename Format**: Files MUST follow the pattern `sc.<TAFSIR_ID>_<CHAPTER_ID>_<AYA_RANGE>.txt`
  - Example: `sc.123_45_67_69.txt`
  - The tafsir ID extraction depends on this exact format
  
- **Metadata CSV**: The `tafsir-metadata.csv` file contains:
  - tafsir_id, tafsir_title, author_id, author_name, death_dce, place_of_death
  - Supports multiple authors per tafsir (handled by iterating through matching rows)

### Environment Variables

- `METADATA_PATH`: Path to the metadata CSV file (defaults to "tafsir-metadata.csv")

## Data Structure

### Output JSON Format
Each line in the output contains:
- `id`: Unique identifier with format "tafsir.subchapter" + UUID
- `series`: UUID for grouping related documents  
- `tafsir_id`: Extracted from filename
- `tafsir_title`: From metadata CSV
- `author_name`: From metadata CSV (supports multiple authors as author_name_2, etc.)
- `author_death_dce`: Death year in DCE format
- `author_place_of_death`: Location of death
- `text`: Complete text content from the source file