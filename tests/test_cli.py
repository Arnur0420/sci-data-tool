from pathlib import Path

from sci_tool.cli import main

SAMPLE = Path(__file__).parent.parent / "data" / "sample.csv"


def test_cli_success_creates_plots(tmp_path, capsys):
    code = main([str(SAMPLE), "--output", str(tmp_path)])
    out = capsys.readouterr().out
    assert code == 0
    assert "Regression" in out
    assert (tmp_path / "regression.png").exists()
    assert (tmp_path / "histogram.png").exists()


def test_cli_reports_cleaning(tmp_path, capsys):
    main([str(SAMPLE), "--output", str(tmp_path)])
    out = capsys.readouterr().out
    assert "Loaded 10 rows, 8 after cleaning" in out


def test_cli_missing_file(tmp_path, capsys):
    code = main(["no_such_file.csv", "--output", str(tmp_path)])
    assert code == 1
    assert "File not found" in capsys.readouterr().err


def test_cli_missing_column(tmp_path, capsys):
    code = main([str(SAMPLE), "--x", "zzz", "--output", str(tmp_path)])
    assert code == 1
    assert "Column not found" in capsys.readouterr().err