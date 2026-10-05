"""Command-line interface: ``member-reader`` or ``python -m member_reader``."""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence

from . import __version__
from .errors import MemberReaderError
from .export import to_csv, to_json
from .query import filter_members
from .reader import load_members


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="member-reader",
        description="Read, validate, filter and export a members CSV file.",
    )
    parser.add_argument("file", help="path to the members CSV file")
    parser.add_argument("--gender", help="only members with this gender (case-insensitive)")
    parser.add_argument("--domain", help="only members whose email is at this domain")
    parser.add_argument("--search", help="only members whose full name contains this text")
    parser.add_argument(
        "--format",
        choices=("names", "json", "csv"),
        default="names",
        help="output format (default: names, one per line)",
    )
    parser.add_argument(
        "--skip-invalid",
        action="store_true",
        help="skip rows that fail validation instead of exiting with an error",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        members = load_members(args.file, on_error="skip" if args.skip_invalid else "raise")
    except (MemberReaderError, OSError) as e:
        print(f"member-reader: error: {e}", file=sys.stderr)
        return 1

    selected = list(
        filter_members(
            members, gender=args.gender, email_domain=args.domain, name_contains=args.search
        )
    )

    if args.format == "json":
        print(to_json(selected))
    elif args.format == "csv":
        sys.stdout.write(to_csv(selected))
    else:
        for m in selected:
            print(m.full_name)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
