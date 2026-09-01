"""演習3の模範解答: ディレクトリ内の.logファイル一覧をサイズ順に取得する"""

from pathlib import Path


def list_log_files_with_size(dir_path):
    """指定ディレクトリ直下にある拡張子 .log のファイルを、サイズの降順で一覧にする。

    詳しい仕様は exercises/exercise3.py の docstring を参照してください。
    """
    dir_path = Path(dir_path)

    results = []
    for entry in dir_path.iterdir():
        if entry.is_file() and entry.suffix == ".log":
            results.append((entry.name, entry.stat().st_size))

    # サイズ(タプルの2番目の要素)の降順で並べ替える
    results.sort(key=lambda item: item[1], reverse=True)

    return results
