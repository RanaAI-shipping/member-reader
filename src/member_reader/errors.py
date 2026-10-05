"""Exceptions raised by member_reader.

Every exception inherits from :class:`MemberReaderError`, so callers can catch
that single type to handle any problem with the input data.
"""

from __future__ import annotations

from collections.abc import Iterable


class MemberReaderError(Exception):
    """Base class for all errors raised by this package."""


class MissingColumnsError(MemberReaderError):
    """The CSV header is missing one or more required columns.

    Attributes:
        missing: The required column names that were not found, sorted.
    """

    def __init__(self, missing: Iterable[str]) -> None:
        self.missing = sorted(missing)
        super().__init__(f"CSV is missing required column(s): {', '.join(self.missing)}")


class InvalidRowError(MemberReaderError):
    """A data row contains a value that failed validation.

    Attributes:
        line: 1-based line number in the source file (the header is line 1).
        field: Name of the column that failed validation.
        value: The raw value that was rejected.
        reason: Human-readable explanation.
    """

    def __init__(self, line: int, field: str, value: str, reason: str) -> None:
        self.line = line
        self.field = field
        self.value = value
        self.reason = reason
        super().__init__(f"line {line}: invalid {field} {value!r}: {reason}")
