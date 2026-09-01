"""演習3(list_log_files_with_size)のテスト。"""
from exercises.exercise3 import list_log_files_with_size


def test_list_log_files_sorted_by_size_desc(tmp_path):
    (tmp_path / "small.log").write_text("a" * 10, encoding="utf-8")
    (tmp_path / "large.log").write_text("b" * 100, encoding="utf-8")
    (tmp_path / "medium.log").write_text("c" * 50, encoding="utf-8")
    # .log 以外の拡張子は、たとえサイズが一番大きくても結果に含まれない
    (tmp_path / "notes.txt").write_text("d" * 1000, encoding="utf-8")

    result = list_log_files_with_size(tmp_path)

    assert result == [
        ("large.log", 100),
        ("medium.log", 50),
        ("small.log", 10),
    ]


def test_list_log_files_ignores_subdirectories(tmp_path):
    (tmp_path / "top.log").write_text("x" * 5, encoding="utf-8")
    sub_dir = tmp_path / "sub"
    sub_dir.mkdir()
    (sub_dir / "nested.log").write_text("y" * 999, encoding="utf-8")

    result = list_log_files_with_size(tmp_path)

    # サブディレクトリの中の nested.log は対象外(直下だけを見る)
    assert result == [("top.log", 5)]


def test_list_log_files_empty_dir(tmp_path):
    assert list_log_files_with_size(tmp_path) == []


def test_list_log_files_no_log_files(tmp_path):
    (tmp_path / "readme.txt").write_text("hello", encoding="utf-8")

    assert list_log_files_with_size(tmp_path) == []


def test_list_log_files_accepts_str_path(tmp_path):
    (tmp_path / "a.log").write_text("z" * 3, encoding="utf-8")

    result = list_log_files_with_size(str(tmp_path))

    assert result == [("a.log", 3)]


def test_list_log_files_return_type(tmp_path):
    (tmp_path / "a.log").write_text("z", encoding="utf-8")

    result = list_log_files_with_size(tmp_path)

    assert isinstance(result, list)
    assert isinstance(result[0], tuple)
    assert isinstance(result[0][0], str)
    assert isinstance(result[0][1], int)
