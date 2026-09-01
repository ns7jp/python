"""演習1の模範解答: ログ行をファイルに追記する"""


def write_log_line(file_path, timestamp, level, message):
    """指定したファイルに、ログを1行だけ追記モードで書き込む。

    詳しい仕様は exercises/exercise1.py の docstring を参照してください。
    """
    line = f"[{timestamp}] [{level}] {message}\n"
    with open(file_path, "a", encoding="utf-8") as f:
        f.write(line)
