"""Command-line interface for sci-data-tool."""
import argparse
import sys
from pathlib import Path

from sci_tool.loader import clean_data, load_csv
from sci_tool.plots import plot_histogram, plot_regression
from sci_tool.stats import describe, linear_regression


def build_parser():
    """Create the argument parser."""
    parser = argparse.ArgumentParser(
        prog="sci_tool",
        description="Analyze and visualize experimental data from a CSV file.",
    )
    parser.add_argument("csv_path", help="path to the input CSV file")
    parser.add_argument("--x", default="x", help="name of the x column")
    parser.add_argument("--y", default="y", help="name of the y column")
    parser.add_argument(
        "--output", default="output", help="directory for saved plots"
    )
    parser.add_argument(
        "--bins", type=int, default=10, help="number of histogram bins"
    )
    return parser


def run(args):
    """Run the analysis for parsed arguments and print the results.

    Raises FileNotFoundError or ValueError on invalid input.
    """
    raw = load_csv(args.csv_path)
    df = clean_data(raw)
    print(f"Loaded {len(raw)} rows, {len(df)} after cleaning")

    for column in (args.x, args.y):
        if column not in df.columns:
            raise ValueError(f"Column not found: {column}")

    stats = describe(df[args.y])
    print(f"Statistics for '{args.y}':")
    for key, value in stats.items():
        print(f"  {key}: {value:.4g}")

    fit = linear_regression(df[args.x], df[args.y])
    print(
        f"Regression: y = {fit['slope']:.4f} * x + {fit['intercept']:.4f}, "
        f"R2 = {fit['r2']:.4f}"
    )

    out_dir = Path(args.output)
    reg_path = plot_regression(
        df[args.x], df[args.y], fit, out_dir / "regression.png"
    )
    hist_path = plot_histogram(
        df[args.y], out_dir / "histogram.png", bins=args.bins
    )
    print(f"Saved: {reg_path}")
    print(f"Saved: {hist_path}")


def main(argv=None):
    """Entry point. Returns 0 on success and 1 on error."""
    args = build_parser().parse_args(argv)
    try:
        run(args)
    except (FileNotFoundError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    return 0
