"""演習3の模範解答: JSON形式のレスポンスを解析する

仕様の詳細はexercises/exercise3.pyのdocstringを参照してください。
"""
import json

_ALLOWED_KEYS = ("status", "cpu", "memory")


def parse_server_status_json(json_text):
    """JSON文字列をパースし、サーバー状態に関する情報だけを辞書で返す。

    仕様はexercises/exercise3.pyのdocstringを参照。
    """
    try:
        data = json.loads(json_text)
    except json.JSONDecodeError:
        return {}

    if not isinstance(data, dict):
        return {}

    return {key: data[key] for key in _ALLOWED_KEYS if key in data}
