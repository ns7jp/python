"""演習1(check_port_status)のテスト。"""
from exercises.exercise1 import check_port_status


def test_system_port_lower_bound():
    assert check_port_status(0) == "システムポート"


def test_system_port_typical():
    # SSHの標準ポート
    assert check_port_status(22) == "システムポート"


def test_system_port_upper_bound():
    assert check_port_status(1023) == "システムポート"


def test_registered_port_lower_bound():
    assert check_port_status(1024) == "登録済みポート"


def test_registered_port_typical():
    # 開発用Webサーバーなどでよく使われるポート
    assert check_port_status(8080) == "登録済みポート"


def test_registered_port_upper_bound():
    assert check_port_status(49151) == "登録済みポート"


def test_dynamic_port_lower_bound():
    assert check_port_status(49152) == "動的ポート"


def test_dynamic_port_upper_bound():
    assert check_port_status(65535) == "動的ポート"


def test_invalid_port_negative():
    assert check_port_status(-1) == "無効なポート"


def test_invalid_port_too_large():
    assert check_port_status(70000) == "無効なポート"
