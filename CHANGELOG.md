# Changelog

All notable changes to this project are documented here.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the project uses [Semantic Versioning](https://semver.org/).

## [Unreleased]

## [0.1.0] - 2026-10-06

### Added
- `load_members` / `iter_members` read and validate member CSV files from a path or an open file object.
- `Member` dataclass with typed fields and `full_name`, `email_domain` and `to_dict()` helpers.
- Validation errors (`MissingColumnsError`, `InvalidRowError`) that report the line number and column, plus an `on_error="skip"` mode.
- `filter_members` and `find_by_id` query helpers.
- `to_json` and `to_csv` exporters.
- `member-reader` command-line tool.

[Unreleased]: https://github.com/RanaAI-shipping/member-reader/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/RanaAI-shipping/member-reader/releases/tag/v0.1.0
