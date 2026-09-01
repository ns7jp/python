"""pytest の共通設定ファイル。

このファイルが置かれているディレクトリ(tests)の親ディレクトリではなく、
「このファイルが置かれているディレクトリと同じ階層にある exercises パッケージ」
を import できるようにするため、tests ディレクトリ自身を sys.path の先頭に追加します。

こうしておくことで、tests/test_exerciseN.py の中で
    from exercises.exercise1 import calc_disk_usage_percent
のように書けるようになります。
"""

import os
import sys

# このファイル(conftest.py)が置かれているディレクトリの絶対パスを取得する
THIS_DIR = os.path.dirname(__file__)

# sys.path の先頭に追加する(先頭に入れることで確実に優先的に探索される)
if THIS_DIR not in sys.path:
    sys.path.insert(0, THIS_DIR)
