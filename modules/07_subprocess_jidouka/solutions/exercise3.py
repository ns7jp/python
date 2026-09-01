"""演習3の模範解答: pingコマンドの出力テキストを解析する

仕様の詳細はexercises/exercise3.pyのdocstringを参照してください。
"""


def parse_ping_output(ping_output):
    """pingコマンドの標準出力を模したテキストを解析し、到達可能かを返す。

    仕様はexercises/exercise3.pyのdocstringを参照。
    """
    return "0% packet loss" in ping_output
