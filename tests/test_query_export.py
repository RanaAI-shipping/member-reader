import json
from pathlib import Path

from member_reader import Member, filter_members, find_by_id, load_members, to_csv, to_json


def ids(members: object) -> list[int]:
    return [m.id for m in members]  # type: ignore[attr-defined]


def test_filter_by_gender_case_insensitive(members: list[Member]) -> None:
    assert ids(filter_members(members, gender="female")) == [1, 3]


def test_filter_by_domain_case_insensitive(members: list[Member]) -> None:
    assert ids(filter_members(members, email_domain="@EXAMPLE.com")) == [1, 3]


def test_filter_by_name(members: list[Member]) -> None:
    assert ids(filter_members(members, name_contains="TUR")) == [2]


def test_filter_combines_criteria(members: list[Member]) -> None:
    assert ids(filter_members(members, gender="female", name_contains="grace")) == [3]


def test_filter_without_criteria_returns_all(members: list[Member]) -> None:
    assert ids(filter_members(members)) == [1, 2, 3, 4]


def test_find_by_id(members: list[Member]) -> None:
    found = find_by_id(members, 2)
    assert found is not None and found.last_name == "Turing"
    assert find_by_id(members, 99) is None


def test_to_json(members: list[Member], tmp_path: Path) -> None:
    out = tmp_path / "m.json"
    text = to_json(members[:1], out)
    expected = [
        {
            "id": 1,
            "first_name": "Ada",
            "last_name": "Lovelace",
            "email": "ada@example.com",
            "gender": "Female",
            "ip_address": "192.0.2.1",
        }
    ]
    assert json.loads(text) == expected
    assert json.loads(out.read_text()) == expected


def test_csv_round_trip(members: list[Member], tmp_path: Path) -> None:
    out = tmp_path / "m.csv"
    to_csv(members, out)
    assert load_members(out) == members
