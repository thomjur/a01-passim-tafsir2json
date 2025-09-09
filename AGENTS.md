# Repository Guidelines

## Project Structure & Module Organization
- `main.py` — CLI and core transformation logic (metadata merge, JSONL output).
- `data/` — input `.txt` subchapter files. Naming: `sc.<TAFSIR_ID>_<SURA>_<AYA_START>_<AYA_END>.txt`.
- `json/` — outputs `passim_input.json` (JSON Lines).
- `tafsir-metadata.csv` — bibliographic metadata.
- `tests/` — unit tests (e.g., `tests/test_main.py`).
- `README.md` — usage and context. `pyproject.toml` — tooling config.

## Build, Test, and Development Commands
- Run script (no tags): `uv run main.py`
- Run with tags: `uv run main.py --sura 2 --aya 255`
- Unittests: `uv run python -m unittest -v`
- Pytest (optional): `uv run pytest`
- Lint: `uv run ruff check .`
- Format: `uv run ruff format .`

## Coding Style & Naming Conventions
- Python 3.12+. Use type hints and concise docstrings for all functions.
- 4‑space indentation, readable names (`snake_case` for functions/vars; `CapWords` for classes).
- Keep I/O pure: functions should accept inputs and return/append results without global side effects beyond `OUTPUT_FILE_PATH`.
- Respect filename pattern for inputs; do not mutate input filenames.

## Testing Guidelines
- Frameworks: `unittest` (primary), `pytest` supported.
- Place tests under `tests/`, named `test_*.py` and methods `test_*`.
- Add tests for new CLI behavior and parsing utilities; keep fixtures lightweight (use `tempfile` and `unittest.mock`).
- Run `uv run python -m unittest -v` before opening a PR.

## Commit & Pull Request Guidelines
- Prefer clear, imperative commit messages (e.g., "Fix argparse; add docstrings").
- PRs must include:
  - Summary of changes and rationale
  - Test results (paste output) and any new tests
  - Notes on CLI or README changes, if applicable

## Security & Configuration Tips
- Configure metadata path via `METADATA_PATH` env var when needed.
- Keep large raw data only in `data/`; output goes to `json/passim_input.json`.
- Do not commit secrets or private datasets; respect `.gitignore`.
- Validate input filenames; skip files that don’t match the expected pattern.
