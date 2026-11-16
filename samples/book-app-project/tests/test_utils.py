import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import utils


def test_get_book_details_retries_blank_fields(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    answers = iter(["", "Dune", " ", "Frank Herbert", "1965"])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))

    details = utils.get_book_details()

    assert details == ("Dune", "Frank Herbert", 1965)
    output = capsys.readouterr().out
    assert "Title cannot be empty." in output
    assert "Author cannot be empty." in output


def test_get_book_details_retries_invalid_year(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    answers = iter(["Dune", "Frank Herbert", "unknown", "-1", "1965"])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))

    details = utils.get_book_details()

    assert details == ("Dune", "Frank Herbert", 1965)
    output = capsys.readouterr().out
    assert "Please enter a whole number" in output
    assert "non-negative number" in output


def test_get_book_details_allows_unknown_year(monkeypatch: pytest.MonkeyPatch) -> None:
    answers = iter(["Dune", "Frank Herbert", ""])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))

    assert utils.get_book_details() == ("Dune", "Frank Herbert", 0)
