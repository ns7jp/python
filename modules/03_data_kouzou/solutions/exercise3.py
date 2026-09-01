"""演習3の模範解答: 重複したIPアドレスを取り除く"""


def unique_ip_addresses(ip_list):
    """IPアドレスのリストから重複を取り除き、昇順に並べ替えて返す。

    詳しい仕様は exercises/exercise3.py の docstring を参照してください。
    """
    return sorted(set(ip_list))
