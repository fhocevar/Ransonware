"""Testes determinísticos, sem captura real de teclado."""
import csv
from datetime import datetime
import pytest
from keylogger.event_store import EventCounter, HEADERS, initialize_log, record_event


def read_rows(path):
    with path.open(encoding="utf-8", newline="") as stream:
        return list(csv.reader(stream))


def test_initialize_log_creates_parent_and_header(tmp_path):
    path = tmp_path / "nested" / "events.csv"
    initialize_log(path)
    assert read_rows(path) == [list(HEADERS)]


def test_record_event_writes_expected_csv(tmp_path):
    path = tmp_path / "events.csv"
    initialize_log(path)
    stamp = datetime(2026, 11, 2, 13, 50, 12, 123000)
    assert record_event(path, 1, timestamp=stamp) == "2026-11-02T13:50:12.123"
    assert read_rows(path)[1] == ["2026-11-02T13:50:12.123", "KEY_PRESS", "1"]


def test_record_event_rejects_invalid_count(tmp_path):
    path = tmp_path / "events.csv"
    initialize_log(path)
    with pytest.raises(ValueError):
        record_event(path, 0)
    assert len(read_rows(path)) == 1


def test_counter_counts_and_stops_at_limit(tmp_path):
    path = tmp_path / "events.csv"
    counter = EventCounter(path, max_events=2)
    assert counter.on_press(object()) is None
    assert counter.on_press(object()) is False
    assert counter.on_press(object()) is False
    assert counter.count == 2
    assert len(read_rows(path)) == 3


def test_counter_does_not_store_key_contents(tmp_path):
    path = tmp_path / "events.csv"
    counter = EventCounter(path, max_events=1)
    counter.on_press("SEGREDO_FICTICIO_NAO_PERSISTIR")
    assert "SEGREDO_FICTICIO_NAO_PERSISTIR" not in path.read_text(encoding="utf-8")


@pytest.mark.parametrize("limit", [0, -1, 10001])
def test_invalid_limits(tmp_path, limit):
    with pytest.raises(ValueError):
        EventCounter(tmp_path / "events.csv", max_events=limit)


def test_csv_event_numbers_are_sequential(tmp_path):
    path = tmp_path / "events.csv"
    counter = EventCounter(path, max_events=3)
    for _ in range(3):
        counter.on_press(None)
    assert [row[2] for row in read_rows(path)[1:]] == ["1", "2", "3"]
