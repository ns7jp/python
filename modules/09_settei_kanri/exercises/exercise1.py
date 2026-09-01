"""演習1: JSON設定ファイルを読み込む(難易度: ★☆☆)"""

import json
import os


def load_json_config(file_path):
    """指定したJSONファイルを読み込み、辞書(dict)として返す。

    サーバーの設定ファイルはJSON形式で書かれることがよくあります。
    この関数では、JSONファイルのパスを受け取り、その中身をPythonの
    辞書として読み込んで返す処理を実装してください。

    仕様:
        - file_path で指定されたファイルが存在する場合は、
          json.load() などを使ってファイルの中身を読み込み、
          dict として返す。
        - file_path で指定されたファイルが存在しない場合は、
          エラーを発生させず、空の辞書 {} を返す。

    引数:
        file_path (str): 読み込みたいJSONファイルのパス。

    戻り値:
        dict: JSONファイルの中身を表す辞書。
              ファイルが存在しない場合は空の辞書 {}。

    入出力例:
        # config.json の中身が以下の場合
        # {"host": "localhost", "port": 8080}
        >>> load_json_config("config.json")
        {'host': 'localhost', 'port': 8080}

        >>> load_json_config("not_exist.json")
        {}
    """
    # TODO: file_path が存在するかどうかを os.path.exists() などで確認する
    # TODO: 存在する場合は open() と json.load() でファイルを読み込み、dictを返す
    # TODO: 存在しない場合は空の辞書 {} を返す
    raise NotImplementedError("load_json_config を実装してください")
