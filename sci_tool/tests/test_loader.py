from pathlib import Path

import pytest

from sci_tool.loader import clean_data, load_csv

SAMPLE = Path(__file__).parent.parent / "data" / "sample.csv"


def test_load_csv_reads_file():
    df = load_csv(SAMPLE)
    assert list(df.columns) == ["x", "y"]
    assert len(df) == 10


def test_load_csv_missing_file():
    with pytest.raises(FileNotFoundError):
        load_csv("no_such_file.csv")


def test_clean_data_removes_duplicates_and_nan():
    df = clean_data(load_csv(SAMPLE))
    assert len(df) == 8
    assert not df.isna().any().any()