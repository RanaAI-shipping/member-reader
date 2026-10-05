"""Writing members out as JSON or CSV."""

from __future__ import annotations

import csv
import io
import json
import os
from collections.abc import Iterable

from .models import Member
from .reader import REQUIRED_COLUMNS


def to_json(
    members: Iterable[Member],
    path: str | os.PathLike[str] | None = None,
    *,
    indent: int | None = 2,
) -> str:
    """Serialise members to a JSON array of objects.

    Args:
        members: Members to export.
        path: If given, the JSON is also written to this file (UTF-8).
        indent: Passed to :func:`json.dumps`; use ``None`` for compact output.

    Returns:
        The JSON text.
    """
    text = json.dumps([m.to_dict() for m in members], indent=indent, ensure_ascii=False)
    if path is not None:
        with open(path, "w", encoding="utf-8") as f:
            f.write(text + "\n")
    return text


def to_csv(members: Iterable[Member], path: str | os.PathLike[str] | None = None) -> str:
    """Serialise members to CSV with the standard header.

    The output can be read back with :func:`load_members`.

    Args:
        members: Members to export.
        path: If given, the CSV is also written to this file (UTF-8).

    Returns:
        The CSV text.
    """
    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=REQUIRED_COLUMNS, lineterminator="\n")
    writer.writeheader()
    writer.writerows(m.to_dict() for m in members)
    text = buf.getvalue()
    if path is not None:
        with open(path, "w", encoding="utf-8", newline="") as f:
            f.write(text)
    return text
