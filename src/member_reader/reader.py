"""Reading and validating members from CSV."""

from __future__ import annotations

import csv
import ipaddress
import os
import re
from collections.abc import Iterator
from contextlib import ExitStack
from typing import Literal, TextIO

from .errors import InvalidRowError, MissingColumnsError
from .models import Member

#: Columns that must be present in the CSV header. Extra columns are ignored.
REQUIRED_COLUMNS: tuple[str, ...] = (
    "id",
    "first_name",
    "last_name",
    "email",
    "gender",
    "ip_address",
)

# Deliberately permissive: one "@", no whitespace, and a dot in the domain.
_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

Source = str | os.PathLike[str] | TextIO
OnError = Literal["raise", "skip"]


def iter_members(source: Source, *, on_error: OnError = "raise") -> Iterator[Member]:
    """Lazily yield validated :class:`Member` objects from a CSV source.

    Use this instead of :func:`load_members` for large files, since rows are
    parsed one at a time.

    Args:
        source: A file path, or an already-open text file object (for example
            ``open(...)`` or ``io.StringIO``). Paths are opened as UTF-8.
        on_error: ``"raise"`` (default) raises :class:`InvalidRowError` on the
            first bad row. ``"skip"`` silently drops invalid rows.

    Raises:
        MissingColumnsError: The header lacks a column in ``REQUIRED_COLUMNS``.
        InvalidRowError: A row failed validation and ``on_error="raise"``.
        FileNotFoundError: ``source`` is a path that does not exist.
    """
    if on_error not in ("raise", "skip"):
        raise ValueError(f"on_error must be 'raise' or 'skip', not {on_error!r}")

    with ExitStack() as stack:
        # Only close files we opened ourselves; caller-provided objects stay open.
        f: TextIO = (
            stack.enter_context(open(source, newline="", encoding="utf-8"))
            if isinstance(source, (str, os.PathLike))
            else source
        )
        reader = csv.DictReader(f)
        missing = set(REQUIRED_COLUMNS) - set(reader.fieldnames or ())
        if missing:
            raise MissingColumnsError(missing)

        for row in reader:
            try:
                yield _parse_row(row, reader.line_num)
            except InvalidRowError:
                if on_error == "raise":
                    raise


def load_members(source: Source, *, on_error: OnError = "raise") -> list[Member]:
    """Read every member from a CSV source into a list.

    Accepts the same arguments and raises the same errors as
    :func:`iter_members`.

    Example:
        >>> members = load_members("members.csv")
        >>> members[0].full_name
        'Claresta Reeders'
    """
    return list(iter_members(source, on_error=on_error))


def _parse_row(row: dict[str, str | None], line: int) -> Member:
    values = {col: (row.get(col) or "").strip() for col in REQUIRED_COLUMNS}

    for col in ("first_name", "last_name", "email"):
        if not values[col]:
            raise InvalidRowError(line, col, values[col], "must not be empty")

    try:
        member_id = int(values["id"])
    except ValueError:
        raise InvalidRowError(line, "id", values["id"], "must be an integer") from None

    if not _EMAIL_RE.match(values["email"]):
        raise InvalidRowError(line, "email", values["email"], "not a valid email address")

    try:
        ip = ipaddress.ip_address(values["ip_address"])
    except ValueError:
        raise InvalidRowError(
            line, "ip_address", values["ip_address"], "not a valid IPv4 or IPv6 address"
        ) from None

    return Member(
        id=member_id,
        first_name=values["first_name"],
        last_name=values["last_name"],
        email=values["email"],
        gender=values["gender"],
        ip_address=ip,
    )
