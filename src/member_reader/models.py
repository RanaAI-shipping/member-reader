"""Data model for a single member record."""

from __future__ import annotations

import ipaddress
from dataclasses import dataclass
from typing import Any

IPAddress = ipaddress.IPv4Address | ipaddress.IPv6Address


@dataclass(frozen=True, slots=True)
class Member:
    """One row of a members CSV file, validated and typed.

    Instances are immutable and hashable, so they can be stored in sets or
    used as dictionary keys.

    Attributes:
        id: Unique integer identifier.
        first_name: Given name.
        last_name: Family name.
        email: Email address (validated for basic ``local@domain.tld`` shape).
        gender: Free-text gender value, stored exactly as it appears in the file.
        ip_address: Parsed IPv4 or IPv6 address.
    """

    id: int
    first_name: str
    last_name: str
    email: str
    gender: str
    ip_address: IPAddress

    @property
    def full_name(self) -> str:
        """First and last name joined by a single space."""
        return f"{self.first_name} {self.last_name}"

    @property
    def email_domain(self) -> str:
        """The lower-cased part of the email after ``@``."""
        return self.email.rsplit("@", 1)[-1].lower()

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serialisable dict using the CSV column names as keys."""
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "gender": self.gender,
            "ip_address": str(self.ip_address),
        }
