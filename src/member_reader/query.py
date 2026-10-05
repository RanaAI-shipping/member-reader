"""Filtering and lookup helpers for collections of members."""

from __future__ import annotations

from collections.abc import Iterable, Iterator

from .models import Member


def filter_members(
    members: Iterable[Member],
    *,
    gender: str | None = None,
    email_domain: str | None = None,
    name_contains: str | None = None,
) -> Iterator[Member]:
    """Yield members matching **all** of the given criteria.

    Criteria left as ``None`` are not applied. All comparisons are
    case-insensitive.

    Args:
        members: Any iterable of members, e.g. from :func:`load_members` or
            :func:`iter_members`.
        gender: Exact gender match, e.g. ``"female"``.
        email_domain: Exact domain match after ``@``, e.g. ``"example.com"``.
        name_contains: Substring to look for in the member's full name.

    Example:
        >>> list(filter_members(members, gender="female", name_contains="ann"))
    """
    gender_l = gender.lower() if gender is not None else None
    domain_l = email_domain.lower().lstrip("@") if email_domain is not None else None
    needle = name_contains.lower() if name_contains is not None else None

    for m in members:
        if gender_l is not None and m.gender.lower() != gender_l:
            continue
        if domain_l is not None and m.email_domain != domain_l:
            continue
        if needle is not None and needle not in m.full_name.lower():
            continue
        yield m


def find_by_id(members: Iterable[Member], member_id: int) -> Member | None:
    """Return the first member with ``member_id``, or ``None`` if absent.

    This is a linear scan. For repeated lookups, build an index once instead:
    ``by_id = {m.id: m for m in members}``.
    """
    return next((m for m in members if m.id == member_id), None)
