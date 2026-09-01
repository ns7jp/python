"""
第6章: 例外処理とロギング - サンプルコード

このサンプルでは、以下のポイントを実際に動かしながら確認します。

    1. try/except/else/finally の基本
    2. 複数のexcept節(例外の種類ごとに処理を分ける)
    3. 独自例外クラス(Exceptionを継承したクラス)とraise
    4. loggingモジュールの基本(getLogger, FileHandler, Formatter, レベル設定)
    5. 例外処理とロギングを組み合わせた実践例(リトライ処理)

実行方法:
    cd /home/user/python
    python3 modules/06_reigai_logging/examples/example.py
"""
import logging
import os
import tempfile


# ---------------------------------------------------------------------------
# 1. try/except/else/finally の基本
# ---------------------------------------------------------------------------
def read_config_value(config, key):
    """try/except/else/finallyの4つのブロックの役割を確認するための関数。

    - try: 例外が起きるかもしれない処理を書く
    - except: try節で指定した例外が発生したときだけ実行される
    - else: try節で例外が発生しなかったときだけ実行される
    - finally: 例外が起きても起きなくても、必ず最後に実行される
      (「後片付け」の処理を書くのによく使われる)
    """
    try:
        value = config[key]
    except KeyError:
        print(f"  [except] 設定キー '{key}' が見つかりませんでした")
        value = None
    else:
        print(f"  [else]   設定キー '{key}' の値は {value!r} でした")
    finally:
        print(f"  [finally] '{key}' の確認処理が終わりました")
    return value


# ---------------------------------------------------------------------------
# 2. 複数のexcept節
# ---------------------------------------------------------------------------
def convert_and_divide(value_str, divisor):
    """複数のexcept節で、異なる種類の例外を個別に処理する例。

    文字列を整数に変換してから割り算をする、という2段階の処理には
    それぞれ別の失敗パターンがある。

    - int(value_str) が失敗する場合 -> ValueError
    - 0で割ろうとする場合            -> ZeroDivisionError

    このように、except節は上から順に「どの例外クラスに一致するか」が
    調べられ、最初に一致したブロックだけが実行される。
    """
    try:
        number = int(value_str)
        result = number / divisor
    except ValueError:
        print(f"  [except ValueError] '{value_str}' は整数に変換できません")
        return None
    except ZeroDivisionError:
        print(f"  [except ZeroDivisionError] {divisor} で割ることはできません")
        return None
    else:
        print(f"  [else] {number} / {divisor} = {result}")
        return result


# ---------------------------------------------------------------------------
# 3. 独自例外クラスとraise
# ---------------------------------------------------------------------------
class DiskSpaceError(Exception):
    """ディスクの空き容量が不足していることを表す独自例外。

    Exceptionクラスを継承するだけで、自分のプログラム専用の例外クラスを
    作ることができる。標準の例外(ValueErrorなど)ではなく専用の例外を
    使うことで、「何が原因のエラーなのか」がコードを読むだけで
    分かりやすくなる。
    """

    pass


def check_disk_usage(percent):
    """ディスク使用率が90%以上ならDiskSpaceErrorをraiseする。"""
    if percent >= 90:
        raise DiskSpaceError(f"ディスク使用率が危険水準です({percent}%)")
    return f"ディスク使用率は正常範囲内です({percent}%)"


# ---------------------------------------------------------------------------
# 4. loggingモジュールの基本
# ---------------------------------------------------------------------------
def build_demo_logger(log_file_path):
    """FileHandlerとFormatterを設定したロガーを組み立てて返す。

    - logging.getLogger(name): 名前付きのロガー(記録係)を取得する
    - logger.setLevel(...): このロガーが処理する最低レベルを決める
      (DEBUG < INFO < WARNING < ERROR < CRITICAL の順に重大度が上がる)
    - logging.FileHandler(path): ログの出力先をファイルにするハンドラ
    - logging.Formatter(...): ログの書式(何をどんな順番で出力するか)
    """
    logger = logging.getLogger("example_server_monitor")
    logger.setLevel(logging.INFO)  # INFOより低いDEBUGは記録されない

    # 何度もこの関数を呼んでもハンドラが重複しないようにする
    if not logger.handlers:
        handler = logging.FileHandler(log_file_path, mode="w", encoding="utf-8")
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger


# ---------------------------------------------------------------------------
# 5. 例外処理とロギングを組み合わせた実践例(リトライ処理)
# ---------------------------------------------------------------------------
def demo_retry_operation(logger, fail_times):
    """最初のfail_times回は失敗し、それ以降は成功する処理を模した関数。

    サーバー監視ツールなどでは、一時的な不調で処理が失敗しても
    「失敗をログに記録しつつ、あきらめずに再挑戦する」という設計が
    よく使われる。ここではその考え方を、例外処理とloggingを組み合わせて
    体験する。
    """
    attempts = {"count": 0}

    def flaky_operation():
        attempts["count"] += 1
        if attempts["count"] <= fail_times:
            raise ConnectionError(f"{attempts['count']}回目: 接続に失敗しました")
        return "サーバーへの接続に成功しました"

    max_attempts = fail_times + 2
    last_error = None
    for attempt in range(1, max_attempts + 1):
        try:
            result = flaky_operation()
        except Exception as exc:
            logger.warning(f"{attempt}回目の試行が失敗しました: {exc}")
            last_error = exc
            continue
        else:
            print(f"  {attempt}回目で成功: {result}")
            return result

    # ここに来るのは全部失敗したとき
    raise last_error


def main():
    print("=" * 60)
    print("1. try/except/else/finally の基本")
    print("=" * 60)
    config = {"host": "192.168.1.10", "port": 8080}
    read_config_value(config, "host")
    read_config_value(config, "timeout")  # 存在しないキー

    print()
    print("=" * 60)
    print("2. 複数のexcept節")
    print("=" * 60)
    convert_and_divide("100", 5)
    convert_and_divide("abc", 5)
    convert_and_divide("100", 0)

    print()
    print("=" * 60)
    print("3. 独自例外クラスとraise")
    print("=" * 60)
    print(f"  {check_disk_usage(45)}")
    try:
        check_disk_usage(95)
    except DiskSpaceError as e:
        print(f"  [except DiskSpaceError] {e}")

    print()
    print("=" * 60)
    print("4. loggingモジュールの基本")
    print("=" * 60)
    log_path = os.path.join(tempfile.gettempdir(), "python_kiso_06_example.log")
    logger = build_demo_logger(log_path)

    logger.debug("これはDEBUGログです(レベル設定によりファイルには残らない)")
    logger.info("サーバー監視処理を開始しました")
    logger.warning("応答がやや遅いサーバーがあります")
    logger.error("サーバーX への接続に失敗しました")

    # ハンドラをflushして、確実にファイルへ書き込ませる
    for handler in logger.handlers:
        handler.flush()

    print(f"  ログファイル: {log_path}")
    print("  --- ログファイルの中身 ---")
    with open(log_path, encoding="utf-8") as f:
        for line in f:
            print(f"  {line.rstrip()}")

    print()
    print("=" * 60)
    print("5. 例外処理とロギングを組み合わせた実践例(リトライ処理)")
    print("=" * 60)
    demo_retry_operation(logger, fail_times=2)


if __name__ == "__main__":
    main()
