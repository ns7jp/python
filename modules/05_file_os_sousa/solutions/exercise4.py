"""演習4の模範解答: 削除候補となる古いログファイルを一覧する

この関数は削除候補を一覧するだけで、実際にファイルを削除する処理
(os.remove など)は絶対に行わない、安全設計の関数である。
"""

from pathlib import Path


def find_old_log_candidates(dir_path, max_files_to_keep):
    """更新日時が新しい順に max_files_to_keep 件を残し、それ以外を削除候補として返す。

    詳しい仕様は exercises/exercise4.py の docstring を参照してください。
    この関数は削除候補を一覧するだけで、実際にファイルを削除する処理は
    行わない安全設計であり、内部で os.remove() などは呼び出さない。
    """
    dir_path = Path(dir_path)

    log_files = [
        entry
        for entry in dir_path.iterdir()
        if entry.is_file() and entry.suffix == ".log"
    ]

    # 更新日時(st_mtime)が新しい順(降順)に並べ替える
    log_files.sort(key=lambda entry: entry.stat().st_mtime, reverse=True)

    # 上位 max_files_to_keep 件(残す対象)を除いた残りが削除候補
    candidates = log_files[max_files_to_keep:]

    # ここでは名前を一覧するだけで、実際の削除は一切行わない
    return [entry.name for entry in candidates]
