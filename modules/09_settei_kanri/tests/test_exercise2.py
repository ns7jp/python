"""演習2 load_ini_config のテスト"""

from exercises.exercise2 import load_ini_config


INI_CONTENT = """[server]
host = localhost
port = 8080

[database]
name = mydb
user = admin
"""


def test_load_ini_config_existing_file(tmp_path):
    """存在するiniファイルを {セクション: {キー: 値}} に変換できること"""
    file_path = tmp_path / "server.ini"
    file_path.write_text(INI_CONTENT, encoding="utf-8")

    result = load_ini_config(str(file_path))

    assert result == {
        "server": {"host": "localhost", "port": "8080"},
        "database": {"name": "mydb", "user": "admin"},
    }


def test_load_ini_config_missing_file(tmp_path):
    """存在しないファイルを指定した場合は空の辞書を返すこと"""
    file_path = tmp_path / "not_exist.ini"

    result = load_ini_config(str(file_path))

    assert result == {}


def test_load_ini_config_single_section(tmp_path):
    """セクションが1つだけの場合も正しく変換できること"""
    content = "[app]\nname = myapp\nversion = 1.0\n"
    file_path = tmp_path / "app.ini"
    file_path.write_text(content, encoding="utf-8")

    result = load_ini_config(str(file_path))

    assert result == {"app": {"name": "myapp", "version": "1.0"}}


def test_load_ini_config_no_sections(tmp_path):
    """セクションが1つも無いiniファイルの場合は空の辞書を返すこと"""
    file_path = tmp_path / "empty.ini"
    file_path.write_text("", encoding="utf-8")

    result = load_ini_config(str(file_path))

    assert result == {}
