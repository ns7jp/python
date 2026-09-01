"""演習2のテスト: check_http_status

外部ネットワークには一切アクセスせず、http_get引数にダミー関数を渡す
(依存性注入)ことで、通信結果をシミュレーションしてテストする。
"""
from exercises.exercise2 import check_http_status


class _DummyResponse:
    """requestsのResponseオブジェクトに似せた、テスト用のダミークラス。"""

    def __init__(self, status_code):
        self.status_code = status_code


def test_check_http_status_returns_status_code_on_success():
    def dummy_get(url):
        return _DummyResponse(200)

    assert check_http_status("http://example.local/health", http_get=dummy_get) == 200


def test_check_http_status_returns_404_status_code():
    def dummy_get(url):
        return _DummyResponse(404)

    assert check_http_status("http://example.local/missing", http_get=dummy_get) == 404


def test_check_http_status_returns_none_on_exception():
    def dummy_get_that_fails(url):
        raise ConnectionError("接続できません(テスト用のダミーエラー)")

    result = check_http_status("http://example.local/", http_get=dummy_get_that_fails)
    assert result is None


def test_check_http_status_passes_url_to_http_get():
    received = {}

    def dummy_get(url):
        received["url"] = url
        return _DummyResponse(200)

    check_http_status("http://example.local/status", http_get=dummy_get)
    assert received["url"] == "http://example.local/status"


def test_check_http_status_uses_requests_get_by_default(monkeypatch):
    # http_getを渡さない場合はrequests.getが使われることを、
    # requests.get自体をモックして確認する(実際の通信は行わない)
    import requests

    def fake_requests_get(url):
        return _DummyResponse(201)

    monkeypatch.setattr(requests, "get", fake_requests_get)

    assert check_http_status("http://example.local/") == 201
