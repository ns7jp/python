"""pytest の共通設定ファイル。

このファイルが置かれているディレクトリ(tests/)の1つ上の階層、つまり
この章のトップディレクトリを sys.path の先頭に追加します。
こうすることで、テストコードの中で `from exercises.exercise1 import ...` の
ようにパッケージとしてインポートできるようになります。
"""

import os
import sys

# このファイル(conftest.py)が置かれているディレクトリの絶対パスを取得
THIS_DIR = os.path.dirname(os.path.abspath(__file__))

# 1つ上の階層(章のトップディレクトリ = exercises/ solutions/ と同じ階層)
CHAPTER_DIR = os.path.dirname(THIS_DIR)

# sys.path の先頭にまだ入っていなければ追加する
if CHAPTER_DIR not in sys.path:
    sys.path.insert(0, CHAPTER_DIR)
