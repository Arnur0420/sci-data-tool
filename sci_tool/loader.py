"""Loading and cleaning of experimental data from CSV files."""
from pathlib import Path

import pandas as pd


def load_csv(path):
    """Read a CSV file into a DataFrame.

    Raises FileNotFoundError if the file does not exist.
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    return pd.read_csv(path)


def clean_data(df):
    """Drop duplicate rows and rows with missing values."""
    return df.drop_duplicates().dropna().reset_index(drop=True)