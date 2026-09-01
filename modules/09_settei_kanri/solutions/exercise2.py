"""演習2の模範解答: iniファイルを読み込む"""

import configparser
import os


def load_ini_config(file_path):
    """指定したiniファイルを読み込み、入れ子の辞書として返す。

    仕様の詳細は exercises/exercise2.py の docstring を参照してください。
    """
    # ファイルが存在しない場合は空の辞書を返す
    if not os.path.exists(file_path):
        return {}

    parser = configparser.ConfigParser()
    parser.read(file_path, encoding="utf-8")

    result = {}
    for section_name in parser.sections():
        # 各セクションの中身を {キー: 値} の辞書に変換する
        result[section_name] = dict(parser.items(section_name))

    return result
