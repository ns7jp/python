"""演習2(build_service_port_map, find_service_by_port)のテスト。"""
from exercises.exercise2 import build_service_port_map, find_service_by_port


def test_build_basic():
    pairs = [("ssh", 22), ("http", 80), ("https", 443)]
    assert build_service_port_map(pairs) == {"ssh": 22, "http": 80, "https": 443}


def test_build_empty():
    assert build_service_port_map([]) == {}


def test_build_overwrite_duplicate_key():
    # 同じサービス名が2回出てきた場合、後の値で上書きされる
    pairs = [("http", 80), ("http", 8080)]
    assert build_service_port_map(pairs) == {"http": 8080}


def test_build_returns_dict_type():
    result = build_service_port_map([("ssh", 22)])
    assert isinstance(result, dict)


def test_find_service_found():
    port_map = {"ssh": 22, "http": 80, "https": 443}
    assert find_service_by_port(port_map, 80) == "http"


def test_find_service_not_found():
    port_map = {"ssh": 22, "http": 80, "https": 443}
    assert find_service_by_port(port_map, 9999) is None


def test_find_service_empty_map():
    assert find_service_by_port({}, 22) is None


def test_find_service_other_port():
    port_map = {"ssh": 22, "http": 80, "https": 443}
    assert find_service_by_port(port_map, 22) == "ssh"
    assert find_service_by_port(port_map, 443) == "https"
