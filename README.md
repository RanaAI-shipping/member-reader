# member-reader

[![CI](https://github.com/RanaAI-shipping/member-reader/actions/workflows/ci.yml/badge.svg)](https://github.com/RanaAI-shipping/member-reader/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/python-3.11%20%7C%203.12%20%7C%203.13-blue)
![License: MIT](https://img.shields.io/badge/license-MIT-green)

Read, validate, filter and export member records stored as CSV, as a Python library or from the command line.

- **Typed results.** Each row becomes an immutable `Member` with a parsed `int` id and an `ipaddress` object.
- **Validation with line numbers.** Bad data raises a clear error, such as `line 42: invalid email 'bob@': not a valid email address`, or you can skip bad rows.
- **Filtering and lookup** by gender, email domain, name or id.
- **Export** to JSON or CSV.
- **No dependencies.** It uses only the standard library and ships type hints (`py.typed`).

## Installation

Requires Python 3.11 or newer.

```sh
# From GitHub
pip install git+https://github.com/RanaAI-shipping/member-reader.git

# Pin to a release tag (recommended for applications)
pip install "member-reader @ git+https://github.com/RanaAI-shipping/member-reader.git@v0.1.0"
```

In a `requirements.txt` or `pyproject.toml` dependency list:

```
member-reader @ git+https://github.com/RanaAI-shipping/member-reader.git@v0.1.0
```

## Quick start

```python
from member_reader import load_members, filter_members, find_by_id, to_json

members = load_members("members.csv")

print(len(members))  # 1000
print(members[0].full_name)  # Claresta Reeders
print(repr(members[0].ip_address))  # IPv4Address('221.72.113.47')

# Filter (all criteria are optional, case-insensitive, and combined with AND)
women_at_php = list(filter_members(members, gender="Female", email_domain="php.net"))

# Look up by id
m = find_by_id(members, 42)

# Export
to_json(women_at_php, "women_at_php.json")
```

### Handling invalid data

```python
from member_reader import load_members, InvalidRowError, MissingColumnsError, MemberReaderError

try:
    members = load_members("members.csv")
except MissingColumnsError as e:
    print("Bad header, missing:", e.missing)
except InvalidRowError as e:
    print(f"Problem on line {e.line} in column {e.field!r}: {e.reason}")

# Or drop invalid rows silently:
members = load_members("members.csv", on_error="skip")

# Catch every data error from this package with the base class:
try:
    load_members("members.csv")
except MemberReaderError as e:
    ...
```

### Large files

`load_members` reads everything into a list. `iter_members` yields one member at a time and keeps memory use flat:

```python
from member_reader import iter_members, filter_members

for m in filter_members(iter_members("huge.csv"), email_domain="example.com"):
    print(m.email)
```

### Reading from something other than a file path

Any open text file object works, including uploads, `io.StringIO` and HTTP response bodies:

```python
import io
from member_reader import load_members

members = load_members(io.StringIO(csv_text))
```

## CSV format

The first row must be a header containing these columns. Their order doesn't matter, and extra columns are ignored.

| Column       | Type after parsing                 | Validation                                      |
|--------------|------------------------------------|-------------------------------------------------|
| `id`         | `int`                              | must be an integer                              |
| `first_name` | `str`                              | must not be empty                               |
| `last_name`  | `str`                              | must not be empty                               |
| `email`      | `str`                              | must look like `local@domain.tld`               |
| `gender`     | `str`                              | free text, stored as written (may be empty)     |
| `ip_address` | `IPv4Address` \| `IPv6Address`     | must be a valid IPv4 or IPv6 address            |

Files are read as UTF-8. Leading and trailing whitespace is stripped from every value. See [`examples/members.csv`](examples/members.csv) for a 1,000-row example. It's synthetic data generated for testing.

## API reference

Everything below can be imported directly from `member_reader`.

### Reading

| Function | Description |
|---|---|
| `load_members(source, *, on_error="raise") -> list[Member]` | Read every row into a list. |
| `iter_members(source, *, on_error="raise") -> Iterator[Member]` | Yield rows lazily. |
| `REQUIRED_COLUMNS` | Tuple of the required header names. |

- `source` is a file path (`str` or `pathlib.Path`) or an open text file object.
- `on_error` is `"raise"` (stop at the first invalid row) or `"skip"` (drop invalid rows).

### `Member`

A frozen, hashable dataclass.

| Attribute / method | Type | Notes |
|---|---|---|
| `id` | `int` | |
| `first_name`, `last_name`, `email`, `gender` | `str` | |
| `ip_address` | `IPv4Address \| IPv6Address` | |
| `full_name` | `str` (property) | `"First Last"` |
| `email_domain` | `str` (property) | lower-cased part after `@` |
| `to_dict()` | `dict[str, Any]` | JSON-safe, keys match the CSV columns |

### Querying

| Function | Description |
|---|---|
| `filter_members(members, *, gender=None, email_domain=None, name_contains=None) -> Iterator[Member]` | Members matching **all** given criteria (case-insensitive). |
| `find_by_id(members, member_id) -> Member \| None` | First member with that id. Uses a linear scan. For many lookups, build `{m.id: m for m in members}`. |

### Exporting

| Function | Description |
|---|---|
| `to_json(members, path=None, *, indent=2) -> str` | JSON array of objects. Also writes to `path` if given. |
| `to_csv(members, path=None) -> str` | CSV with the standard header, which `load_members` can read back. Also writes to `path` if given. |

### Exceptions

```
MemberReaderError            base class: catch this to handle any data problem
├── MissingColumnsError      .missing: list[str]
└── InvalidRowError          .line: int, .field: str, .value: str, .reason: str
```

The library doesn't catch file-system errors such as `FileNotFoundError`. They reach your code unchanged.

## Command-line usage

Installing the package also installs a `member-reader` command (or run `python -m member_reader`):

```sh
member-reader members.csv                                   # print full names
member-reader members.csv --gender female --format json     # filter, output JSON
member-reader members.csv --domain php.net --format csv     # filter, output CSV
member-reader members.csv --search ann                      # name contains "ann"
member-reader members.csv --skip-invalid                    # ignore bad rows
member-reader --help
```

It exits with code `0` on success and `1` on a data or file error. Error messages go to stderr.

## Development

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

[MIT](LICENSE)
