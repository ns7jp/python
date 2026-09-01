"""演習3の模範解答: 接続リトライ処理のシミュレーション"""


def retry_connection(max_retries, is_success_sequence):
    """接続リトライ処理をシミュレーションする。

    詳しい仕様は exercises/exercise3.py の docstring を参照してください。
    """
    attempt = 0
    while attempt < max_retries:
        if attempt >= len(is_success_sequence):
            # シミュレーション用のデータが尽きた場合も失敗として扱う
            break
        if is_success_sequence[attempt]:
            return f"接続成功({attempt + 1}回目)"
        attempt += 1
    return "接続失敗: リトライ上限到達"
