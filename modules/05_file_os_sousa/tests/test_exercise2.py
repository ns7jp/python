"""演習2(extract_error_lines)のテスト。"""
from exercises.exercise2 import extract_error_lines


def test_extract_only_error_lines(tmp_path):
    log_file = tmp_path / "app.log"
    log_file.write_text(
        "[2026-09-01 10:00:00] [INFO] 起動しました\n"
        "[2026-09-01 10:01:00] [ERROR] 接続に失敗しました\n"
        "[2026-09-01 10:02:00] [WARNING] メモリ使用率が高いです\n"
        "[2026-09-01 10:03:00] [ERROR] タイムアウトしました\n",
        encoding="utf-8",
    )

    result = extract_error_lines(log_file)

    assert result == [
        "[2026-09-01 10:01:00] [ERROR] 接続に失敗しました",
        "[2026-09-01 10:03:00] [ERROR] タイムアウトしました",
    ]


def test_extract_no_error_lines(tmp_path):
    log_file = tmp_path / "app.log"
    log_file.write_text("[2026-09-01 10:00:00] [INFO] 問題ありません\n", encoding="utf-8")

    assert extract_error_lines(log_file) == []


def test_extract_empty_file(tmp_path):
    log_file = tmp_path / "empty.log"
    log_file.write_text("", encoding="utf-8")

    assert extract_error_lines(log_file) == []


def test_extract_strips_newline(tmp_path):
    log_file = tmp_path / "app.log"
    log_file.write_text("[2026-09-01] [ERROR] テスト\n", encoding="utf-8")

    result = extract_error_lines(log_file)

    assert result == ["[2026-09-01] [ERROR] テスト"]
    assert "\n" not in result[0]


def test_extract_last_line_without_trailing_newline(tmp_path):
    log_file = tmp_path / "app.log"
    # 最終行に改行がないファイルでも正しく処理できることを確認する
    log_file.write_text("[1] [INFO] ok\n[2] [ERROR] ng", encoding="utf-8")

    result = extract_error_lines(log_file)

    assert result == ["[2] [ERROR] ng"]


def test_extract_accepts_str_path(tmp_path):
    log_file = tmp_path / "app.log"
    log_file.write_text("[x] [ERROR] y\n", encoding="utf-8")

    result = extract_error_lines(str(log_file))

    assert result == ["[x] [ERROR] y"]
