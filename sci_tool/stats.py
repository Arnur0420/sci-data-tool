"""Descriptive statistics and linear regression."""
import numpy as np


def describe(values):
    """Return count, mean, sample std, min and max of a 1D sequence.

    Raises ValueError if the sequence is empty.
    """
    arr = np.asarray(values, dtype=float)
    if arr.size == 0:
        raise ValueError("values must not be empty")
    return {
        "count": int(arr.size),
        "mean": float(arr.mean()),
        "std": float(arr.std(ddof=1)) if arr.size > 1 else 0.0,
        "min": float(arr.min()),
        "max": float(arr.max()),
    }


def linear_regression(x, y):
    """Fit y = slope * x + intercept by least squares.

    Returns a dict with slope, intercept and r2 (coefficient of determination).
    Raises ValueError for inputs of different length, fewer than two points,
    or constant x.
    """
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    if x.size != y.size:
        raise ValueError("x and y must have the same length")
    if x.size < 2:
        raise ValueError("at least two points are required")
    if np.ptp(x) == 0:
        raise ValueError("x must not be constant")

    slope, intercept = np.polyfit(x, y, 1)
    predicted = slope * x + intercept
    ss_res = np.sum((y - predicted) ** 2)
    ss_tot = np.sum((y - y.mean()) ** 2)
    r2 = 1.0 if ss_tot == 0 else 1 - ss_res / ss_tot
    return {
        "slope": float(slope),
        "intercept": float(intercept),
        "r2": float(r2),
    }
