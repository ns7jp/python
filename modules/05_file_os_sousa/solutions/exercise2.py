"""演習2の模範解答: ログファイルからエラー行だけを抽出する"""


def extract_error_lines(file_path):
    """指定したファイルを読み込み、"ERROR" を含む行だけをリストで返す。

    詳しい仕様は exercises/exercise2.py の docstring を参照してください。
    """
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # splitlines() を使うと、\n や \r\n などの改行文字を取り除いた状態で
    # 行のリストを取得できる(最終行に改行がない場合にも対応できる)。
    lines = content.splitlines()

    return [line for line in lines if "ERROR" in line]
