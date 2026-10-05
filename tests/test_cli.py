import json
import subprocess
import sys
from pathlib import Path

import pytest

from member_reader.cli import main


def test_names_default(valid_csv: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert main([str(valid_csv)]) == 0
    assert capsys.readouterr().out.splitlines()[0] == "Ada Lovelace"


def test_filter_and_json(valid_csv: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert main([str(valid_csv), "--gender", "male", "--format", "json"]) == 0
    assert [m["id"] for m in json.loads(capsys.readouterr().out)] == [2]


def test_csv_output(valid_csv: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert main([str(valid_csv), "--search", "hopper", "--format", "csv"]) == 0
    assert capsys.readouterr().out.splitlines()[1].startswith("3,Grace,Hopper")


def test_runs_as_module(valid_csv: Path) -> None:
    result = subprocess.run(
        [sys.executable, "-m", "member_reader", str(valid_csv)],
        capture_output=True,
        text=True,
        check=True,
    )
    assert result.stdout.startswith("Ada Lovelace")


def test_error_exit_code(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    bad = tmp_path / "bad.csv"
    bad.write_text("id,first_name\n1,A\n")
    assert main([str(bad)]) == 1
    assert "missing required column" in capsys.readouterr().err
