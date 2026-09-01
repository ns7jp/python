"""演習3の模範解答: モジュール分割 - データセンターの温度レポートを作る

仕様の詳細はexercises/exercise3.pyのdocstringを参照してください。
"""
from exercises.utils import celsius_to_status


def datacenter_temperature_report(temps):
    """複数の気温データから、それぞれの状態をまとめたレポート(リスト)を作る。

    仕様はexercises/exercise3.pyのdocstringを参照。
    """
    return [celsius_to_status(temp) for temp in temps]
