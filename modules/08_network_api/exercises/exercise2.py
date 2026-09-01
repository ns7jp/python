"""演習2: requestsライブラリで外部APIやWebサーバーの状態を確認する

サーバー監視ツールでは、「Webサーバーがちゃんと200 OKを返しているか」
「監視対象のAPIが正常に応答しているか」をHTTP通信で確認することが
よくあります。この演習では、`requests`ライブラリを使ってURLにGET
リクエストを送り、HTTPステータスコードを取得する関数を作ります。

重要なポイントは「依存性注入(いそんせいちゅうにゅう)」という設計です。
関数の中で直接`requests.get`を呼び出すのではなく、「HTTP通信を行う関数」を
引数として外から渡せるようにしておくことで、テストのときには実際に
ネットワーク通信を行わない「ダミーの関数」に差し替えることができます。
これにより、外部ネットワークに一切アクセスせずに関数の動作をテストできます。
"""
import requests


def check_http_status(url, http_get=None):
    """指定したURLにGETリクエストを送り、HTTPステータスコードを返す。

    http_get引数に関数が渡された場合は、実際の通信の代わりにその関数を
    使ってリクエストを行います(依存性注入)。http_get引数が渡されな
    かった場合(None)は、requests.get を使って本物のHTTP通信を行います。

    http_get(渡す場合)は「urlを受け取り、`.status_code`属性を持つ
    オブジェクト(requestsのResponseオブジェクトと同じ形)を返す関数」
    として扱ってください。通信中に何らかの例外が発生した場合は、その
    例外を外に投げずにNoneを返してください。

    引数:
        url (str): リクエスト先のURL。
        http_get (callable | None): url を受け取り、`.status_code`
            属性を持つオブジェクトを返す関数。Noneの場合はrequests.get
            が使われる。テスト時にダミー関数を渡すことで、外部ネット
            ワークにアクセスせずにこの関数の動作を確認できる。

    戻り値:
        int | None: 通信に成功した場合はHTTPステータスコード(例: 200,
            404, 500)。通信中に例外が発生した場合はNone。

    入出力例:
        >>> class DummyResponse:
        ...     status_code = 200
        >>> check_http_status("http://example.com", http_get=lambda url: DummyResponse())
        200

        >>> def dummy_get_error(url):
        ...     raise ConnectionError("接続できません")
        >>> check_http_status("http://example.com", http_get=dummy_get_error)
        (Noneが返る)

    ヒント:
        - `getter = http_get if http_get is not None else requests.get`
          のように、実際に使う関数を1つの変数にまとめると、以降の処理を
          共通化できます。
        - `try: ... except Exception: return None` で、通信中に起きる
          さまざまな例外(タイムアウト・接続エラーなど)をまとめて
          Noneに変換できます。
    """
    # TODO: http_get が None でなければそれを、None であれば requests.get を
    #       使う関数を選んでください。
    #       try節でその関数にurlを渡して呼び出し、戻り値の.status_codeを
    #       返してください。
    #       例外が発生した場合はexcept節でNoneを返してください。
    raise NotImplementedError("check_http_status を実装してください")
