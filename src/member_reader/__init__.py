"""Read, validate, filter and export member records stored as CSV.

Quick start::

    from member_reader import load_members, filter_members

    members = load_members("members.csv")
    for m in filter_members(members, email_domain="example.com"):
        print(m.full_name, m.email)
"""

from .errors import InvalidRowError, MemberReaderError, MissingColumnsError
from .export import to_csv, to_json
from .models import Member
from .query import filter_members, find_by_id
from .reader import REQUIRED_COLUMNS, iter_members, load_members

__version__ = "0.1.0"

__all__ = [
    "REQUIRED_COLUMNS",
    "InvalidRowError",
    "Member",
    "MemberReaderError",
    "MissingColumnsError",
    "__version__",
    "filter_members",
    "find_by_id",
    "iter_members",
    "load_members",
    "to_csv",
    "to_json",
]
