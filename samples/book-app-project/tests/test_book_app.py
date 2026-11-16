import os
import sys
from pathlib import Path

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import book_app
import books
from books import BookCollection


@pytest.fixture
def collection(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> BookCollection:
    data_file = tmp_path / "data.json"
    data_file.write_text("[]", encoding="utf-8")
    monkeypatch.setattr(books, "DATA_FILE", str(data_file))
    return BookCollection()


def test_read_command_marks_book_and_reports_success(
    collection: BookCollection,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    collection.add_book("Dune", "Frank Herbert", 1965)
    monkeypatch.setattr(book_app, "collection", collection)
    monkeypatch.setattr(sys, "argv", ["book_app.py", "read"])
    monkeypatch.setattr("builtins.input", lambda _: "Dune")

    book_app.main()

    assert collection.find_book_by_title("Dune").read is True
    assert "Book marked as read." in capsys.readouterr().out


def test_read_command_reports_missing_book(
    collection: BookCollection,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setattr(book_app, "collection", collection)
    monkeypatch.setattr("builtins.input", lambda _: "Unknown title")

    book_app.handle_mark_as_read()

    assert 'Book "Unknown title" not found.' in capsys.readouterr().out
