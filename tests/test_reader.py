import io
import ipaddress
from pathlib import Path

import pytest
from conftest import HEADER

from member_reader import (
    InvalidRowError,
    MemberReaderError,
    MissingColumnsError,
    iter_members,
    load_members,
)


def test_load_from_path(valid_csv: Path) -> None:
    members = load_members(valid_csv)
    assert [m.id for m in members] == [1, 2, 3, 4]
    assert members[0].full_name == "Ada Lovelace"
    assert members[1].ip_address == ipaddress.IPv6Address("2001:db8::1")


def test_load_from_str_path(valid_csv: Path) -> None:
    assert len(load_members(str(valid_csv))) == 4


def test_load_from_file_object() -> None:
    f = io.StringIO(HEADER + "1,A,B,a@b.co,X,10.0.0.1\n")
    assert load_members(f)[0].email == "a@b.co"


def test_iter_is_lazy(valid_csv: Path) -> None:
    it = iter_members(valid_csv)
    assert next(it).id == 1


def test_extra_columns_ignored_and_whitespace_stripped() -> None:
    f = io.StringIO(
        "id,first_name,last_name,email,gender,ip_address,notes\n"
        " 7 , Ann , Lee ,ann@x.io,F,10.0.0.1,hello\n"
    )
    m = load_members(f)[0]
    assert (m.id, m.first_name, m.last_name) == (7, "Ann", "Lee")


def test_missing_columns() -> None:
    f = io.StringIO("id,first_name\n1,A\n")
    with pytest.raises(MissingColumnsError) as exc:
        load_members(f)
    assert exc.value.missing == ["email", "gender", "ip_address", "last_name"]
    assert isinstance(exc.value, MemberReaderError)


@pytest.mark.parametrize(
    ("row", "field"),
    [
        ("x,A,B,a@b.co,F,10.0.0.1", "id"),
        ("1,,B,a@b.co,F,10.0.0.1", "first_name"),
        ("1,A,B,not-an-email,F,10.0.0.1", "email"),
        ("1,A,B,a@b.co,F,999.1.1.1", "ip_address"),
    ],
)
def test_invalid_row_reports_line_and_field(row: str, field: str) -> None:
    f = io.StringIO(HEADER + "1,Ok,Row,ok@b.co,F,10.0.0.1\n" + row + "\n")
    with pytest.raises(InvalidRowError) as exc:
        load_members(f)
    assert exc.value.line == 3
    assert exc.value.field == field
    assert "line 3" in str(exc.value)


def test_skip_invalid_rows() -> None:
    f = io.StringIO(HEADER + "x,A,B,a@b.co,F,10.0.0.1\n2,C,D,c@d.co,M,10.0.0.2\n")
    assert [m.id for m in load_members(f, on_error="skip")] == [2]


def test_bad_on_error_value(valid_csv: Path) -> None:
    with pytest.raises(ValueError):
        load_members(valid_csv, on_error="ignore")  # type: ignore[arg-type]


def test_missing_file(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        load_members(tmp_path / "nope.csv")


def test_bundled_example_file_is_valid() -> None:
    example = Path(__file__).parents[1] / "examples" / "members.csv"
    assert len(load_members(example)) == 1000
