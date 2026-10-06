"""Plotting helpers that save figures to image files."""
from pathlib import Path

import numpy as np
from matplotlib.figure import Figure


def _save(fig, output_path):
    """Save a figure, creating parent directories if needed."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    return output_path


def plot_regression(x, y, fit, output_path, title="Linear regression"):
    """Draw a scatter plot of the data with the fitted regression line.

    `fit` is the dict returned by `stats.linear_regression`.
    Returns the path of the saved image.
    Raises ValueError for empty input or inputs of different length.
    """
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    if x.size == 0:
        raise ValueError("x and y must not be empty")
    if x.size != y.size:
        raise ValueError("x and y must have the same length")

    fig = Figure(figsize=(6, 4))
    ax = fig.subplots()
    ax.scatter(x, y, label="data")

    xs = np.linspace(x.min(), x.max(), 100)
    label = (
        f"y = {fit['slope']:.3f}x + {fit['intercept']:.3f} "
        f"(R² = {fit['r2']:.3f})"
    )
    ax.plot(xs, fit["slope"] * xs + fit["intercept"], color="red", label=label)

    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title(title)
    ax.legend()
    ax.grid(True, alpha=0.3)
    return _save(fig, output_path)


def plot_histogram(values, output_path, bins=10, title="Histogram"):
    """Draw a histogram of a 1D sequence and save it to a file.

    Returns the path of the saved image.
    Raises ValueError for empty input or bins < 1.
    """
    arr = np.asarray(values, dtype=float)
    if arr.size == 0:
        raise ValueError("values must not be empty")
    if bins < 1:
        raise ValueError("bins must be at least 1")

    fig = Figure(figsize=(6, 4))
    ax = fig.subplots()
    ax.hist(arr, bins=bins, edgecolor="black")
    ax.set_xlabel("value")
    ax.set_ylabel("count")
    ax.set_title(title)
    ax.grid(True, alpha=0.3)
    return _save(fig, output_path)