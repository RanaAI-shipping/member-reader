# Contributing

## Setup

```sh
git clone https://github.com/RanaAI-shipping/member-reader.git
cd member-reader
python3 -m venv .venv          # Python 3.11+
source .venv/bin/activate
pip install -e ".[dev]"
```

## Checks

CI runs all of these on Python 3.11 to 3.13, and each one must pass:

```sh
ruff check .            # lint (ruff check --fix . to auto-fix)
ruff format --check .   # formatting (ruff format . to apply)
mypy                    # strict type checking of src/
pytest                  # tests
```

Run a single test with `pytest tests/test_reader.py::test_missing_columns`.

## Guidelines

- The library has no runtime dependencies. Please keep it that way, or open an issue to discuss first.
- Everything public is exported from `src/member_reader/__init__.py` and documented in the README's API reference. Update both when you change the public API.
- Add an entry under `[Unreleased]` in `CHANGELOG.md` for any user-visible change.

## Releasing

1. Bump `__version__` in `src/member_reader/__init__.py`.
2. Move the `[Unreleased]` changelog entries under a new version heading.
3. Commit, then tag and push: `git tag v0.2.0 && git push --tags`.
4. Create a GitHub release from the tag.
