"""演習3のテスト: ポート番号の妥当性チェック"""

from exercises.exercise3 import is_valid_port


def test_is_valid_port_typical_values():
    assert is_valid_port(22) is True
    assert is_valid_port(8080) is True


def test_is_valid_port_boundary_min():
    assert is_valid_port(0) is True


def test_is_valid_port_boundary_max():
    assert is_valid_port(65535) is True


def test_is_valid_port_out_of_range_high():
    assert is_valid_port(65536) is False
    assert is_valid_port(70000) is False


def test_is_valid_port_out_of_range_negative():
    assert is_valid_port(-1) is False


def test_is_valid_port_rejects_string():
    assert is_valid_port("8080") is False


def test_is_valid_port_rejects_float():
    assert is_valid_port(8080.0) is False
    assert is_valid_port(22.5) is False


def test_is_valid_port_rejects_bool():
    # bool は int のサブクラスだが、ポート番号としては無効とする
    assert is_valid_port(True) is False
    assert is_valid_port(False) is False


def test_is_valid_port_rejects_none():
    assert is_valid_port(None) is False
