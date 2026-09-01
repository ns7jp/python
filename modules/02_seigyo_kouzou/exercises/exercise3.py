"""演習3: 接続リトライ処理のシミュレーション

サーバーへの接続は、ネットワークの一時的な不調などにより1回目で失敗する
ことがあります。そのため実際の運用スクリプトでは「失敗したら少し待って
もう一度試す(リトライする)」という処理がよく使われます。この演習では
while文とカウンタ変数を使って、接続リトライのシミュレーションを実装します。
"""


def retry_connection(max_retries, is_success_sequence):
    """接続リトライ処理をシミュレーションする。

    is_success_sequence はブール値のリストで、i番目(0始まり)の値が
    「i+1回目の接続試行が成功したかどうか」を表す。
    先頭から順に最大 max_retries 回まで試行をシミュレートし、
    成功した時点でその試行回数を含む文字列を返す。

    while文とカウンタ変数を使って実装すること。

    引数:
        max_retries (int): 最大リトライ回数(最大の試行回数)。
        is_success_sequence (list[bool]): i番目の要素が
            i+1回目の試行結果(成功ならTrue)を表すリスト。

    戻り値:
        str:
            - 成功した場合: "接続成功(n回目)" (nは1始まりの試行回数)
            - max_retries回試行しても成功しなかった場合、または
              is_success_sequence の要素数が試行回数に対して
              足りない場合: "接続失敗: リトライ上限到達"

    入出力例:
        >>> retry_connection(5, [False, False, True, False])
        '接続成功(3回目)'
        >>> retry_connection(3, [False, False, False, True])
        '接続失敗: リトライ上限到達'
        >>> retry_connection(5, [False, False])
        '接続失敗: リトライ上限到達'
        >>> retry_connection(3, [True])
        '接続成功(1回目)'
    """
    # TODO: while文とカウンタ変数(例: attempt = 0)を使って実装してください。
    #       ・attempt が max_retries に達したらループを抜ける
    #       ・is_success_sequence の要素数が足りない場合も失敗として扱う
    #       ・is_success_sequence[attempt] が True なら成功メッセージを返す
    raise NotImplementedError("retry_connection を実装してください")
