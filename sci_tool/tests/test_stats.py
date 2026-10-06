from pathlib import Path

import pytest

from sci_tool.loader import clean_data, load_csv
from sci_tool.stats import describe, linear_regression

SAMPLE = Path(__file__).parent.parent / "data" / "sample.csv"


def test_describe_basic():
    result = describe([1, 2, 3, 4, 5])
    assert result["count"] == 5
    assert result["mean"] == pytest.approx(3.0)
    assert result["std"] == pytest.approx(1.5811, abs=1e-3)
    assert result["min"] == 1
    assert result["max"] == 5


def test_describe_single_value():
    assert describe([7])["std"] == 0.0


def test_describe_empty_raises():
    with pytest.raises(ValueError):
        describe([])


def test_regression_perfect_line():
    result = linear_regression([1, 2, 3, 4], [2, 4, 6, 8])
    assert result["slope"] == pytest.approx(2.0)
    assert result["intercept"] == pytest.approx(0.0, abs=1e-9)
    assert result["r2"] == pytest.approx(1.0)


def test_regression_length_mismatch():
    with pytest.raises(ValueError):
        linear_regression([1, 2, 3], [1, 2])


def test_regression_too_few_points():
    with pytest.raises(ValueError):
        linear_regression([1], [1])


def test_regression_constant_x():
    with pytest.raises(ValueError):
        linear_regression([2, 2, 2], [1, 2, 3])


def test_regression_on_sample_data():
    df = clean_data(load_csv(SAMPLE))
    result = linear_regression(df["x"], df["y"])
    assert result["slope"] == pytest.approx(2.0, abs=0.05)
    assert result["r2"] > 0.99