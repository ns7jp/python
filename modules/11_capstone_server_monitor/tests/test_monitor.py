"""総合演習(ミニ・サーバー監視ツール)のテスト

外部ネットワークには一切アクセスせず、以下の方法だけでテストを完結させる。

- ポート疎通確認(check_target_port): 127.0.0.1上に自分で
  ソケットサーバーを一時的に立てる(08章と同じ考え方)。
- HTTP確認(check_target_http, check_target, run_monitor_cycle):
  http_get引数にダミー関数を渡し、実際の通信を行わない
  (依存性注入。08章と同じ考え方)。
- 純粋なロジック(update_failure_counts, get_alerts): 辞書を
  直接組み立ててテストする。
- 設定読み込み(load_config): pytestのtmp_path fixtureで一時的な
  JSONファイルを作成して読み込む。
"""
import json
import logging
import socket

import pytest

from exercises.monitor import (
    check_target,
    check_target_http,
    check_target_port,
    get_alerts,
    load_config,
    log_cycle_result,
    run_monitor_cycle,
    update_failure_counts,
)


# ---------------------------------------------------------------------------
# テスト用の補助関数・クラス
# ---------------------------------------------------------------------------
def _get_free_port_socket():
    """127.0.0.1上で空いているポートにbindしたソケットを返す。

    ポート番号は0を指定することでOSに自動的に選んでもらう
    (08章のtest_exercise1.pyと同じ考え方)。
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("127.0.0.1", 0))
    return s


class _FakeResponse:
    """requestsのResponseもどきの、テスト用ダミークラス。"""

    def __init__(self, status_code):
        self.status_code = status_code


class _RecordingLogger:
    """logger.info / logger.warning が呼ばれたことを記録するダミーロガー。"""

    def __init__(self):
        self.infos = []
        self.warnings = []

    def info(self, message):
        self.infos.append(message)

    def warning(self, message):
        self.warnings.append(message)


# ---------------------------------------------------------------------------
# check_target_port: ローカルソケットサーバーを使ったテスト
# ---------------------------------------------------------------------------
def test_check_target_port_true_when_listening():
    server = _get_free_port_socket()
    port = server.getsockname()[1]
    server.listen(1)
    try:
        assert check_target_port("127.0.0.1", port) is True
    finally:
        server.close()


def test_check_target_port_false_when_nothing_listening():
    # bindだけしてlistenせずにすぐcloseする -> ポートは解放され、
    # 接続を試みるとConnection Refusedになる(何も待ち受けていない)
    server = _get_free_port_socket()
    port = server.getsockname()[1]
    server.close()

    assert check_target_port("127.0.0.1", port) is False


# ---------------------------------------------------------------------------
# check_target_http: http_get引数によるモック
# ---------------------------------------------------------------------------
def test_check_target_http_returns_none_for_no_url():
    assert check_target_http(None) is None
    assert check_target_http("") is None


def test_check_target_http_true_for_200():
    def fake_get(url):
        return _FakeResponse(200)

    assert check_target_http("http://example.com", http_get=fake_get) is True


def test_check_target_http_true_for_2xx():
    def fake_get(url):
        return _FakeResponse(204)

    assert check_target_http("http://example.com", http_get=fake_get) is True


def test_check_target_http_false_for_500():
    def fake_get(url):
        return _FakeResponse(500)

    assert check_target_http("http://example.com", http_get=fake_get) is False


def test_check_target_http_false_on_exception():
    def fake_get(url):
        raise ConnectionError("接続失敗(テスト用)")

    assert check_target_http("http://example.com", http_get=fake_get) is False


# ---------------------------------------------------------------------------
# check_target: ポート・HTTPを組み合わせたテスト
# ---------------------------------------------------------------------------
def test_check_target_healthy_when_port_open_and_no_http():
    server = _get_free_port_socket()
    port = server.getsockname()[1]
    server.listen(1)
    try:
        target = {
            "name": "web-01",
            "host": "127.0.0.1",
            "port": port,
            "http_url": None,
        }
        result = check_target(target)
    finally:
        server.close()

    assert result["name"] == "web-01"
    assert result["port_ok"] is True
    assert result["http_ok"] is None
    assert result["healthy"] is True


def test_check_target_unhealthy_when_port_closed():
    server = _get_free_port_socket()
    port = server.getsockname()[1]
    server.close()

    target = {
        "name": "app-01",
        "host": "127.0.0.1",
        "port": port,
        "http_url": None,
    }
    result = check_target(target)

    assert result["port_ok"] is False
    assert result["healthy"] is False


def test_check_target_unhealthy_when_http_fails_even_if_port_ok():
    server = _get_free_port_socket()
    port = server.getsockname()[1]
    server.listen(1)

    def fake_get(url):
        return _FakeResponse(500)

    try:
        target = {
            "name": "web-01",
            "host": "127.0.0.1",
            "port": port,
            "http_url": "http://127.0.0.1/health",
        }
        result = check_target(target, http_get=fake_get)
    finally:
        server.close()

    assert result["port_ok"] is True
    assert result["http_ok"] is False
    assert result["healthy"] is False


# ---------------------------------------------------------------------------
# run_monitor_cycle: 複数targetをまとめてチェック
# ---------------------------------------------------------------------------
def test_run_monitor_cycle_returns_result_per_target():
    server = _get_free_port_socket()
    port = server.getsockname()[1]
    server.listen(1)

    def fake_get(url):
        return _FakeResponse(200)

    try:
        config = {
            "targets": [
                {
                    "name": "web-01",
                    "host": "127.0.0.1",
                    "port": port,
                    "http_url": "http://127.0.0.1/health",
                },
                {
                    "name": "app-01",
                    "host": "127.0.0.1",
                    "port": port,  # 同じポートを再利用してよい(単なる疎通確認)
                    "http_url": None,
                },
            ]
        }
        results = run_monitor_cycle(config, http_get=fake_get)
    finally:
        server.close()

    assert len(results) == 2
    assert results[0]["name"] == "web-01"
    assert results[0]["healthy"] is True
    assert results[1]["name"] == "app-01"
    assert results[1]["healthy"] is True


def test_run_monitor_cycle_empty_targets():
    assert run_monitor_cycle({"targets": []}) == []


# ---------------------------------------------------------------------------
# update_failure_counts: 純粋なロジック
# ---------------------------------------------------------------------------
def test_update_failure_counts_increments_on_failure():
    results = [{"name": "web-01", "healthy": False}]
    updated = update_failure_counts(results, {"web-01": 2})
    assert updated == {"web-01": 3}


def test_update_failure_counts_resets_on_success():
    results = [{"name": "web-01", "healthy": True}]
    updated = update_failure_counts(results, {"web-01": 5})
    assert updated == {"web-01": 0}


def test_update_failure_counts_new_target_starts_from_zero():
    results = [{"name": "web-01", "healthy": False}]
    updated = update_failure_counts(results, {})
    assert updated == {"web-01": 1}


def test_update_failure_counts_does_not_mutate_input():
    original = {"web-01": 2}
    results = [{"name": "web-01", "healthy": False}]
    updated = update_failure_counts(results, original)

    # 引数のfailure_counts自体は書き換えられていないこと
    assert original == {"web-01": 2}
    assert updated == {"web-01": 3}
    assert updated is not original


def test_update_failure_counts_multiple_targets():
    results = [
        {"name": "web-01", "healthy": False},
        {"name": "app-01", "healthy": True},
    ]
    updated = update_failure_counts(results, {"web-01": 1, "app-01": 4})
    assert updated == {"web-01": 2, "app-01": 0}


# ---------------------------------------------------------------------------
# get_alerts: 純粋なロジック
# ---------------------------------------------------------------------------
def test_get_alerts_returns_names_at_or_above_threshold():
    failure_counts = {"web-01": 3, "app-01": 1, "db-01": 5}
    assert set(get_alerts(failure_counts, threshold=3)) == {"web-01", "db-01"}


def test_get_alerts_returns_empty_when_none_meet_threshold():
    failure_counts = {"web-01": 1, "app-01": 2}
    assert get_alerts(failure_counts, threshold=3) == []


def test_get_alerts_empty_failure_counts():
    assert get_alerts({}, threshold=3) == []


# ---------------------------------------------------------------------------
# log_cycle_result: ダミーロガーで記録内容を確認
# ---------------------------------------------------------------------------
def test_log_cycle_result_logs_info_for_healthy():
    logger = _RecordingLogger()
    results = [
        {"name": "web-01", "port_ok": True, "http_ok": None, "healthy": True}
    ]
    log_cycle_result(logger, results)

    assert len(logger.infos) == 1
    assert len(logger.warnings) == 0
    assert "web-01" in logger.infos[0]


def test_log_cycle_result_logs_warning_for_unhealthy():
    logger = _RecordingLogger()
    results = [
        {"name": "app-01", "port_ok": False, "http_ok": None, "healthy": False}
    ]
    log_cycle_result(logger, results)

    assert len(logger.warnings) == 1
    assert len(logger.infos) == 0
    assert "app-01" in logger.warnings[0]


def test_log_cycle_result_works_with_real_logger(tmp_path):
    # 実際のlogging.Loggerを使っても例外なく動作することを確認する
    log_file = tmp_path / "monitor_test.log"
    logger = logging.getLogger("test_monitor_capstone")
    logger.setLevel(logging.INFO)
    logger.handlers = []
    handler = logging.FileHandler(log_file, encoding="utf-8")
    logger.addHandler(handler)

    results = [
        {"name": "web-01", "port_ok": True, "http_ok": True, "healthy": True},
        {"name": "app-01", "port_ok": False, "http_ok": None, "healthy": False},
    ]
    log_cycle_result(logger, results)
    handler.flush()

    content = log_file.read_text(encoding="utf-8")
    assert "web-01" in content
    assert "app-01" in content


# ---------------------------------------------------------------------------
# load_config: tmp_pathで一時的なJSONファイルを作成してテスト
# ---------------------------------------------------------------------------
def test_load_config_reads_json_file(tmp_path):
    config_data = {
        "targets": [
            {"name": "web-01", "host": "127.0.0.1", "port": 8080, "http_url": None}
        ],
        "alert_threshold_consecutive_failures": 3,
    }
    config_file = tmp_path / "config.json"
    config_file.write_text(json.dumps(config_data), encoding="utf-8")

    loaded = load_config(str(config_file))

    assert loaded == config_data


def test_load_config_returns_dict_type(tmp_path):
    config_file = tmp_path / "config.json"
    config_file.write_text(json.dumps({"targets": []}), encoding="utf-8")

    loaded = load_config(str(config_file))

    assert isinstance(loaded, dict)


def test_load_config_raises_for_missing_file(tmp_path):
    missing_path = tmp_path / "does_not_exist.json"
    with pytest.raises(OSError):
        load_config(str(missing_path))
