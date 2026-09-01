"""演習3(unique_ip_addresses)のテスト。"""
from exercises.exercise3 import unique_ip_addresses


def test_unique_basic():
    ip_list = ["192.168.1.5", "10.0.0.1", "192.168.1.5", "10.0.0.2"]
    assert unique_ip_addresses(ip_list) == ["10.0.0.1", "10.0.0.2", "192.168.1.5"]


def test_unique_no_duplicates():
    ip_list = ["10.0.0.3", "10.0.0.1", "10.0.0.2"]
    assert unique_ip_addresses(ip_list) == ["10.0.0.1", "10.0.0.2", "10.0.0.3"]


def test_unique_all_same():
    ip_list = ["172.16.0.1", "172.16.0.1", "172.16.0.1"]
    assert unique_ip_addresses(ip_list) == ["172.16.0.1"]


def test_unique_empty_list():
    assert unique_ip_addresses([]) == []


def test_unique_returns_list_type():
    result = unique_ip_addresses(["10.0.0.1"])
    assert isinstance(result, list)


def test_unique_single_element():
    assert unique_ip_addresses(["10.0.0.1"]) == ["10.0.0.1"]
