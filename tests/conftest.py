from pathlib import Path

import pytest

from member_reader import Member, load_members

DATA = Path(__file__).parent / "data"
HEADER = "id,first_name,last_name,email,gender,ip_address\n"


@pytest.fixture
def valid_csv() -> Path:
    return DATA / "valid.csv"


@pytest.fixture
def members(valid_csv: Path) -> list[Member]:
    return load_members(valid_csv)
