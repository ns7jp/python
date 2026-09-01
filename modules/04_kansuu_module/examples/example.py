"""
第4章: 関数とモジュール分割 - サンプルコード

このサンプルでは、以下のポイントを実際に動かしながら確認します。

    1. def による関数定義とdocstring
    2. 位置引数・デフォルト引数
    3. 可変長引数(*args)
    4. 戻り値(複数の値をまとめて返す)
    5. 複数ファイルへのモジュール分割とimport(server_utils.py を利用)
    6. デコレーターの基礎(処理時間を計測するデコレーター)

実行方法:
    cd /home/user/python
    python3 modules/04_kansuu_module/examples/example.py

(補足) Pythonはスクリプトを直接実行すると、そのスクリプトが置かれている
ディレクトリを自動的にsys.pathへ追加します。そのため、同じ examples
ディレクトリにある server_utils.py を「import server_utils」という形で
読み込むことができます。
"""
import functools
import time

from server_utils import build_status_line


# ---------------------------------------------------------------------------
# 1. 位置引数とデフォルト引数
# ---------------------------------------------------------------------------
def greet_operator(name, role="オペレーター"):
    """位置引数(name)とデフォルト引数(role)を持つ関数の例。

    role は呼び出し時に省略すると "オペレーター" が使われる。

    引数:
        name (str): 呼びかける相手の名前(位置引数、省略不可)。
        role (str): 相手の役割(デフォルト引数、省略可)。

    戻り値:
        str: 挨拶の文字列。
    """
    return f"こんにちは、{name}さん({role})!"


# ---------------------------------------------------------------------------
# 2. 可変長引数 (*args)
# ---------------------------------------------------------------------------
def total_disk_usage_gb(*usage_list):
    """可変長引数(*args)の例。

    呼び出し側は好きな個数の数値を渡せる。関数の中では usage_list という
    タプルとして受け取れる。

    引数:
        *usage_list (float): 各ディスクの使用量(GB)。0個以上。

    戻り値:
        float: 合計使用量(GB)。引数がなければ 0 を返す。
    """
    return sum(usage_list)


# ---------------------------------------------------------------------------
# 3. 戻り値(複数の値をタプルとしてまとめて返す)
# ---------------------------------------------------------------------------
def summarize_server(name, cpu_percent, memory_percent=0.0):
    """サーバーの状態をまとめて返す関数の例。

    Pythonでは "return a, b, c" のように書くと、複数の値をタプルとして
    まとめて返すことができ、呼び出し側で "a, b, c = f(...)" のように
    まとめて受け取れる。

    引数:
        name (str): サーバー名。
        cpu_percent (float): CPU使用率(%)。
        memory_percent (float): メモリ使用率(%)。デフォルトは0.0。

    戻り値:
        tuple: (name, status, cpu_percent, memory_percent)
    """
    status = "警告" if cpu_percent >= 80 else "正常"
    return name, status, cpu_percent, memory_percent


# ---------------------------------------------------------------------------
# 4. デコレーターの基礎
# ---------------------------------------------------------------------------
def measure_time(func):
    """関数の実行時間を計測して表示するデコレーター。

    デコレーターとは「関数を受け取り、機能を追加した別の関数を返す関数」
    のことです。「@measure_time」と書くだけで、対象の関数の前後に
    時間計測の処理を追加できます。サーバー運用では、処理にかかった時間を
    ログに残したいときなどによく使われる考え方です。

    functools.wraps(func) を使うことで、ラップ後の関数(wrapper)が
    元の関数の __name__ などの情報を保つようにしている。これを忘れると、
    デバッグ時に関数名が "wrapper" と表示されてしまい分かりにくくなる。
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"[実行時間] {func.__name__}: {elapsed:.3f}秒")
        return result

    return wrapper


@measure_time
def slow_health_check(server_name):
    """時間のかかる処理をしているふりをする関数(デコレーターの動作確認用)。"""
    time.sleep(0.2)
    return f"{server_name} は正常に応答しました"


def main():
    print("=" * 60)
    print("1. 位置引数とデフォルト引数")
    print("=" * 60)
    print(greet_operator("田中"))
    print(greet_operator("鈴木", role="新人エンジニア"))

    print()
    print("=" * 60)
    print("2. 可変長引数 (*args)")
    print("=" * 60)
    print(f"合計ディスク使用量: {total_disk_usage_gb(10.5, 20.0, 5.25)} GB")
    print(f"引数なしの場合: {total_disk_usage_gb()} GB")

    print()
    print("=" * 60)
    print("3. 戻り値(複数の値をタプルで受け取る)")
    print("=" * 60)
    name, status, cpu, mem = summarize_server("web01", 85.0, 60.0)
    print(f"{name}: 状態={status}, CPU={cpu}%, メモリ={mem}%")

    print()
    print("=" * 60)
    print("4. モジュール分割とimport (server_utils.pyの関数を利用)")
    print("=" * 60)
    print(build_status_line("db01", "active"))
    print(build_status_line("db02", "stopped"))

    print()
    print("=" * 60)
    print("5. デコレーターの基礎(処理時間計測)")
    print("=" * 60)
    result = slow_health_check("app01")
    print(result)


if __name__ == "__main__":
    main()
