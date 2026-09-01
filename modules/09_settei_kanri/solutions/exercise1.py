"""演習1の模範解答: JSON設定ファイルを読み込む"""

import json
import os


def load_json_config(file_path):
    """指定したJSONファイルを読み込み、辞書(dict)として返す。

    仕様の詳細は exercises/exercise1.py の docstring を参照してください。
    """
    # ファイルが存在しない場合は空の辞書を返す
    if not os.path.exists(file_path):
        return {}

    # ファイルが存在する場合は開いて読み込む
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)
