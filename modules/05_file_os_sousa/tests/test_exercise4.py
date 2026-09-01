"""演習4(find_old_log_candidates)のテスト。"""
import os

from exercises.exercise4 import find_old_log_candidates


def _create_log_with_mtime(path, content, mtime):
    """テスト用: ファイルを作成し、更新日時(mtime)を明示的に設定するヘルパー。"""
    path.write_text(content, encoding="utf-8")
    os.utime(path, (mtime, mtime))


def test_find_old_log_candidates_basic(tmp_path):
    base = 1_700_000_000  # 適当な基準時刻(エポック秒)
    _create_log_with_mtime(tmp_path / "app1.log", "1", base + 300)  # 一番新しい
    _create_log_with_mtime(tmp_path / "app2.log", "2", base + 200)
    _create_log_with_mtime(tmp_path / "app3.log", "3", base + 100)
    _create_log_with_mtime(tmp_path / "app4.log", "4", base + 0)  # 一番古い

    result = find_old_log_candidates(tmp_path, max_files_to_keep=2)

    # 新しい2件(app1.log, app2.log)は残す対象なので削除候補には含まれない
    assert result == ["app3.log", "app4.log"]


def test_find_old_log_candidates_keep_all_when_enough_slots(tmp_path):
    base = 1_700_000_000
    _create_log_with_mtime(tmp_path / "a.log", "x", base)
    _create_log_with_mtime(tmp_path / "b.log", "y", base + 10)

    result = find_old_log_candidates(tmp_path, max_files_to_keep=5)

    assert result == []


def test_find_old_log_candidates_ignores_non_log_files(tmp_path):
    base = 1_700_000_000
    _create_log_with_mtime(tmp_path / "a.log", "x", base)
    _create_log_with_mtime(tmp_path / "b.log", "y", base + 10)
    (tmp_path / "readme.txt").write_text("これはログファイルではない", encoding="utf-8")

    result = find_old_log_candidates(tmp_path, max_files_to_keep=1)

    assert result == ["a.log"]


def test_find_old_log_candidates_does_not_delete_files(tmp_path):
    """安全設計であることの確認: 呼び出してもファイルは一切削除されない。"""
    base = 1_700_000_000
    _create_log_with_mtime(tmp_path / "a.log", "x", base)
    _create_log_with_mtime(tmp_path / "b.log", "y", base + 10)

    find_old_log_candidates(tmp_path, max_files_to_keep=0)

    assert (tmp_path / "a.log").exists()
    assert (tmp_path / "b.log").exists()


def test_find_old_log_candidates_empty_dir(tmp_path):
    assert find_old_log_candidates(tmp_path, max_files_to_keep=3) == []


def test_find_old_log_candidates_accepts_str_path(tmp_path):
    base = 1_700_000_000
    _create_log_with_mtime(tmp_path / "a.log", "x", base)
    _create_log_with_mtime(tmp_path / "b.log", "y", base + 10)

    result = find_old_log_candidates(str(tmp_path), max_files_to_keep=0)

    assert result == ["b.log", "a.log"]
