"""演習1(write_log_line)のテスト。"""
from exercises.exercise1 import write_log_line


def test_write_single_line(tmp_path):
    log_file = tmp_path / "app.log"
    write_log_line(str(log_file), "2026-09-01 10:00:00", "INFO", "起動しました")

    content = log_file.read_text(encoding="utf-8")
    assert content == "[2026-09-01 10:00:00] [INFO] 起動しました\n"


def test_write_appends_multiple_lines(tmp_path):
    log_file = tmp_path / "app.log"
    write_log_line(log_file, "2026-09-01 10:00:00", "INFO", "起動しました")
    write_log_line(log_file, "2026-09-01 10:01:00", "ERROR", "接続に失敗しました")

    lines = log_file.read_text(encoding="utf-8").splitlines()
    assert lines == [
        "[2026-09-01 10:00:00] [INFO] 起動しました",
        "[2026-09-01 10:01:00] [ERROR] 接続に失敗しました",
    ]


def test_write_accepts_path_object(tmp_path):
    log_file = tmp_path / "sub.log"
    write_log_line(log_file, "2026-01-01 00:00:00", "WARNING", "ディスク使用率が高いです")

    assert log_file.exists()
    assert "WARNING" in log_file.read_text(encoding="utf-8")


def test_write_creates_new_file_if_not_exists(tmp_path):
    log_file = tmp_path / "new.log"
    assert not log_file.exists()

    write_log_line(log_file, "2026-01-01 00:00:00", "INFO", "テスト")

    assert log_file.exists()


def test_write_does_not_overwrite_existing_content(tmp_path):
    log_file = tmp_path / "app.log"
    log_file.write_text("[既存の行]\n", encoding="utf-8")

    write_log_line(log_file, "2026-01-01 00:00:00", "INFO", "追記された行")

    content = log_file.read_text(encoding="utf-8")
    assert content == "[既存の行]\n[2026-01-01 00:00:00] [INFO] 追記された行\n"
