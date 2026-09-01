"""pytest用の共通設定(conftest.py)。

このファイル(tests/conftest.py)が置かれているディレクトリ(tests)を
os.path.dirname(__file__) で取得し、その親ディレクトリ、つまり
この章のディレクトリ(modules/02_seigyo_kouzou)自体を
sys.path の先頭に追加する。

これにより、テストコードから `exercises` パッケージを
`from exercises.exercise1 import check_port_status` のような形で
import できるようになる。
"""
import os
import sys

# tests ディレクトリのパス
_TESTS_DIR = os.path.dirname(__file__)
# その親ディレクトリ(章のディレクトリ)を sys.path の先頭に追加する
sys.path.insert(0, os.path.dirname(_TESTS_DIR))
