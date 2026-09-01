"""演習3のテスト: datacenter_temperature_report / celsius_to_status"""
from exercises.exercise3 import datacenter_temperature_report
from exercises.utils import celsius_to_status


def test_celsius_to_status_low():
    assert celsius_to_status(15) == "低温注意"


def test_celsius_to_status_normal():
    assert celsius_to_status(24) == "正常"


def test_celsius_to_status_high():
    assert celsius_to_status(30) == "高温注意"


def test_celsius_to_status_boundaries():
    assert celsius_to_status(20) == "正常"
    assert celsius_to_status(28) == "正常"


def test_datacenter_temperature_report():
    assert datacenter_temperature_report([15, 24, 30]) == [
        "低温注意",
        "正常",
        "高温注意",
    ]


def test_datacenter_temperature_report_empty():
    assert datacenter_temperature_report([]) == []
