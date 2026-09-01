"""演習2: 複数のレスポンスタイムから平均値を求める

サーバー監視では、複数回計測したレスポンスタイム(応答時間)の平均を
求めたい場面がよくあります。この演習では可変長引数(*args)を使って、
何個の値を渡されても平均を計算できる関数を実装します。
"""


def average_response_time(*response_times_ms):
    """複数のレスポンスタイム(ミリ秒)の平均値を計算する。

    可変長引数として、いくつでも数値を受け取れるようにする
    (*response_times_ms は呼び出し時に渡された引数をタプルとしてまとめる)。

    引数:
        *response_times_ms (int | float): レスポンスタイム(ミリ秒)。
            0個以上渡される。

    戻り値:
        float: 平均値を小数点第2位までroundした値。
            引数が1つも渡されなかった場合は 0.0 を返す。

    入出力例:
        >>> average_response_time(100, 200, 300)
        200.0
        >>> average_response_time(120.5, 130.25)
        125.38
        >>> average_response_time()
        0.0
    """
    # TODO: response_times_ms が空の場合は 0.0 を返してください。
    #       それ以外の場合は合計を個数で割って平均値を計算し、
    #       round()を使って小数点第2位まで丸めて返してください。
    raise NotImplementedError("average_response_time を実装してください")
