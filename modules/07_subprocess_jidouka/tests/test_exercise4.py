"""演習4のテスト: build_health_check_script_report"""
import sys

from exercises.exercise4 import build_health_check_script_report


def test_all_services_successful():
    commands = {
        "web": ["echo", "ok"],
        "cache": [sys.executable, "-c", "exit(0)"],
    }
    report = build_health_check_script_report(commands)
    assert report == {"web": True, "cache": True}


def test_mixed_success_and_failure():
    commands = {
        "web": ["echo", "ok"],
        "db": [sys.executable, "-c", "exit(1)"],
    }
    report = build_health_check_script_report(commands)
    assert report == {"web": True, "db": False}


def test_all_services_failed():
    commands = {
        "db": [sys.executable, "-c", "exit(1)"],
        "queue": [sys.executable, "-c", "exit(2)"],
    }
    report = build_health_check_script_report(commands)
    assert report == {"db": False, "queue": False}


def test_returns_dict_with_bool_values():
    commands = {"web": ["echo", "ok"]}
    report = build_health_check_script_report(commands)
    assert isinstance(report, dict)
    assert isinstance(report["web"], bool)


def test_empty_commands_returns_empty_dict():
    assert build_health_check_script_report({}) == {}
