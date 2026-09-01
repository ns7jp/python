"""演習2の模範解答: returncode を見て「成功したかどうか」を判定する

仕様の詳細はexercises/exercise2.pyのdocstringを参照してください。
"""
import subprocess


def is_command_successful(command):
    """外部コマンドを実行し、正常終了(returncode == 0)したかどうかを返す。

    仕様はexercises/exercise2.pyのdocstringを参照。
    """
    result = subprocess.run(command, capture_output=True, text=True)
    return result.returncode == 0
