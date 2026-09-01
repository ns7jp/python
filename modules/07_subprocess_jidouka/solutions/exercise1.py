"""演習1の模範解答: subprocess.run で外部コマンドを実行し、結果を受け取る

仕様の詳細はexercises/exercise1.pyのdocstringを参照してください。
"""
import subprocess


def run_command(command):
    """外部コマンドを実行し、(returncode, 標準出力の文字列) のタプルを返す。

    仕様はexercises/exercise1.pyのdocstringを参照。
    """
    result = subprocess.run(command, capture_output=True, text=True)
    return (result.returncode, result.stdout)
