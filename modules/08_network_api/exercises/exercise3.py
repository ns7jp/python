"""演習3: JSON形式のレスポンスを解析する

多くの監視APIやサーバーの状態確認エンドポイントは、結果を
JSON(JavaScript Object Notation)という形式の文字列で返します。
Python標準ライブラリの`json`モジュールを使うと、JSON文字列をPythonの
辞書(dict)に変換したり、逆に辞書をJSON文字列に変換したりできます。

この演習では、サーバーの状態を表すJSON文字列(例:
`'{"status": "ok", "cpu": 42, "memory": 70}'`)を受け取り、必要な情報
だけを取り出す関数を作ります。監視対象から返ってくるJSONには、想定外の
キーが含まれていることもあれば、通信の乱れで壊れたJSON文字列が返って
くることもあります。そうした場合にもプログラムが落ちないように設計する
ことが、実務では重要です。
"""
import json


def parse_server_status_json(json_text):
    """JSON文字列をパースし、サーバー状態に関する情報だけを辞書で返す。

    引数のjson_textを`json.loads`でパースし、キー"status", "cpu",
    "memory"のうち、実際に存在するものだけを含む新しい辞書を作って
    返してください。存在しないキーは戻り値の辞書にも含めません。

    json_textが不正なJSON文字列で`json.JSONDecodeError`が発生した場合、
    またはパース結果が辞書(dict)ではなかった場合は、空の辞書`{}`を
    返してください(呼び出し元は例外を意識せずに済みます)。

    引数:
        json_text (str): サーバーの状態を表すJSON文字列。

    戻り値:
        dict: "status", "cpu", "memory"のうち存在するキーだけを含む辞書。
            不正なJSONの場合、またはJSONのトップレベルが辞書でない場合は
            空の辞書`{}`。

    入出力例:
        >>> parse_server_status_json('{"status": "ok", "cpu": 42, "memory": 70}')
        {'status': 'ok', 'cpu': 42, 'memory': 70}

        >>> parse_server_status_json('{"status": "ok", "disk": 90}')
        {'status': 'ok'}

        >>> parse_server_status_json('これはJSONではありません')
        {}

        >>> parse_server_status_json('[1, 2, 3]')
        {}
    """
    # TODO: try節でjson.loads(json_text)を呼び出してください。
    #       json.JSONDecodeErrorが発生した場合はexcept節で{}を返してください。
    #       パース結果がdictでない場合も{}を返してください。
    #       パース結果がdictの場合は、"status", "cpu", "memory"のうち
    #       存在するキーだけを含む新しい辞書を作って返してください。
    raise NotImplementedError("parse_server_status_json を実装してください")
