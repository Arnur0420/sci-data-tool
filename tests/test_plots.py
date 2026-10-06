import pytest

from sci_tool.plots import plot_histogram, plot_regression
from sci_tool.stats import linear_regression

X = [1, 2, 3, 4, 5]
Y = [2.1, 3.9, 6.2, 7.8, 10.1]


def test_plot_regression_creates_file(tmp_path):
    out = tmp_path / "reg.png"
    fit = linear_regression(X, Y)
    result = plot_regression(X, Y, fit, out)
    assert result == out
    assert out.exists() and out.stat().st_size > 0


def test_plot_regression_creates_parent_dir(tmp_path):
    out = tmp_path / "nested" / "dir" / "reg.png"
    plot_regression(X, Y, linear_regression(X, Y), out)
    assert out.exists()


def test_plot_regression_length_mismatch(tmp_path):
    fit = linear_regression(X, Y)
    with pytest.raises(ValueError):
        plot_regression([1, 2, 3], [1, 2], fit, tmp_path / "bad.png")


def test_plot_histogram_creates_file(tmp_path):
    out = tmp_path / "hist.png"
    plot_histogram(Y, out, bins=4)
    assert out.exists() and out.stat().st_size > 0


def test_plot_histogram_invalid_input(tmp_path):
    with pytest.raises(ValueError):
        plot_histogram([], tmp_path / "h.png")
    with pytest.raises(ValueError):
        plot_histogram(Y, tmp_path / "h.png", bins=0)