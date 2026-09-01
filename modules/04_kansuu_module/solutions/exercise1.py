"""演習1の模範解答: バイト数を読みやすい単位に変換する

仕様の詳細はexercises/exercise1.pyのdocstringを参照してください。
"""


def human_readable_bytes(size_bytes):
    """バイト数を人間が読みやすい単位の文字列に変換する。

    仕様はexercises/exercise1.pyのdocstringを参照。
    """
    kb = 1024
    mb = kb * 1024
    gb = mb * 1024

    if size_bytes < kb:
        return f"{size_bytes}B"
    elif size_bytes < mb:
        return f"{size_bytes / kb:.2f}KB"
    elif size_bytes < gb:
        return f"{size_bytes / mb:.2f}MB"
    else:
        return f"{size_bytes / gb:.2f}GB"
