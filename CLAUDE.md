# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

`member-reader` is a zero-dependency Python library (3.11+) and CLI for reading, validating, filtering and exporting member records from CSV. It's intended to be installed by other applications from GitHub, so the public API and its documentation are the product.

## Commands

```sh
source .venv/bin/activate        # dev env (Python 3.12); ignore the legacy venv/ (3.9)
pip install -e ".[dev]"          # or: uv pip install -e ".[dev]"

pytest                                         # all tests
pytest tests/test_reader.py::test_missing_columns   # single test
ruff check . && ruff format --check .          # lint + format (CI runs both)
mypy                                           # strict, src/ only
member-reader examples/members.csv --gender female --format json   # try the CLI
```

CI (`.github/workflows/ci.yml`) runs ruff, mypy and pytest on Python 3.11, 3.12 and 3.13.

## Architecture

`src/` layout. The dependency flow is one-directional: `models`/`errors` ← `reader` ← `query`/`export` ← `cli`.

- `reader.py` is the core. `iter_members` is the single parsing path. `load_members` is just `list(iter_members(...))`. `source` may be a path or an open text file; only paths are opened and closed by the library (an `ExitStack` handles this). `REQUIRED_COLUMNS` is the schema, which `export.to_csv` also uses as its header, so CSV export round-trips through `load_members`.
- Validation happens in `_parse_row` and raises `InvalidRowError` with a 1-based file line number (`csv.DictReader.line_num`; the header is line 1). `on_error="skip"` swallows only `InvalidRowError`. `MissingColumnsError` always raises.
- `Member` is a frozen, slotted dataclass. `ip_address` is an `ipaddress` object, so serialization must go through `Member.to_dict()`.
- `query.filter_members` returns a lazy iterator, and all comparisons are case-insensitive.

## Conventions

- The public API is whatever `__init__.py` exports in `__all__`. When you change it, also update the README's "API reference" section and add a `CHANGELOG.md` entry under `[Unreleased]`.
- The version lives only in `src/member_reader/__init__.py` (`__version__`), which hatchling reads dynamically.
- Keep runtime `dependencies = []`. Dev tools go in the `dev` extra.
- `examples/members.csv` is 1,000 rows of synthetic data, and a test asserts it all parses. Unit tests use the small `tests/data/valid.csv` or inline `io.StringIO` CSV.
- GitHub URLs assume the repo is `RanaAI-shipping/member-reader` (in `pyproject.toml`, the README, the CHANGELOG and CONTRIBUTING).
