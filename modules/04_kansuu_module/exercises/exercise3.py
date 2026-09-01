"""演習3: モジュール分割 - データセンターの温度レポートを作る

同じ exercises ディレクトリにある utils.py から celsius_to_status 関数を
importして使います。処理を複数のファイルに分割し、importして組み合わせる
という、実務でもよく使う構成を体験する演習です。
"""
from exercises.utils import celsius_to_status


def datacenter_temperature_report(temps):
    """複数の気温データから、それぞれの状態をまとめたレポート(リスト)を作る。

    temps の各要素を celsius_to_status 関数に渡してステータス文字列に変換し、
    元の並び順のままリストとして返す。

    引数:
        temps (list[int | float]): 気温(℃)のリスト。

    戻り値:
        list[str]: 各気温に対応するステータス文字列
            ("低温注意" / "正常" / "高温注意")のリスト。

    入出力例:
        >>> datacenter_temperature_report([15, 24, 30])
        ['低温注意', '正常', '高温注意']
        >>> datacenter_temperature_report([])
        []
    """
    # TODO: celsius_to_status を使って、temps の各要素をステータス文字列に
    #       変換したリストを作って返してください。
    #       ヒント: リスト内包表記、またはforループ+appendで書けます。
    raise NotImplementedError("datacenter_temperature_report を実装してください")
