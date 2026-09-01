"""演習2: iniファイルを読み込む(難易度: ★★☆)"""

import configparser
import os


def load_ini_config(file_path):
    """指定したiniファイルを読み込み、入れ子の辞書として返す。

    サーバーソフトウェアの設定ファイルには、iniファイル形式
    (例: [section] の下に key = value を並べる形式)がよく使われます。
    configparser を使ってiniファイルを読み込み、
    {セクション名: {キー: 値}} という入れ子の dict に変換してください。

    仕様:
        - file_path で指定されたファイルが存在する場合は、
          configparser.ConfigParser を使って読み込み、
          {セクション名: {キー: 値, ...}, ...} という
          入れ子の dict に変換して返す。
        - [DEFAULT] セクションなど、configparser自体の特殊な
          挙動は気にしなくてよい(通常のセクションだけを変換すればよい)。
        - file_path で指定されたファイルが存在しない場合は、
          エラーを発生させず、空の辞書 {} を返す。
        - キーと値はどちらも文字列(str)のままでよい(型変換は不要)。

    引数:
        file_path (str): 読み込みたいiniファイルのパス。

    戻り値:
        dict: {セクション名: {キー: 値}} という形の入れ子の辞書。
              ファイルが存在しない場合は空の辞書 {}。

    入出力例:
        # server.ini の中身が以下の場合
        # [server]
        # host = localhost
        # port = 8080
        >>> load_ini_config("server.ini")
        {'server': {'host': 'localhost', 'port': '8080'}}

        >>> load_ini_config("not_exist.ini")
        {}
    """
    # TODO: file_path が存在するかどうかを確認する
    # TODO: 存在する場合は configparser.ConfigParser() を作成し、read() で読み込む
    # TODO: parser.sections() でセクション名を取得し、各セクションの items() を
    #       使って {セクション名: {キー: 値}} の形に変換する
    # TODO: 存在しない場合は空の辞書 {} を返す
    raise NotImplementedError("load_ini_config を実装してください")
