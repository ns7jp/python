#!/usr/bin/env python3
"""
第7章: 外部コマンド実行と自動化スクリプト - サンプルコード

このサンプルでは、以下のポイントを実際に動かしながら確認します。

    1. subprocess.run() の基本(capture_output, text, returncode)
    2. returncode を使ったエラーハンドリング(例外を使わない失敗判定)
    3. os.system() を使わない理由(シェルインジェクションの危険性)
    4. シバン行(#!/usr/bin/env python3)と実行権限を持つスクリプト
    5. cronでの定期実行を見越した、複数サービスのヘルスチェック

実行方法:
    cd /home/user/python
    python3 modules/07_subprocess_jidouka/examples/example.py

このサンプルは外部ネットワークに一切アクセスしません。すべて
echo・python3自身(sys.executable)など、Linux環境に標準で存在する
コマンドと、一時ディレクトリ(tempfile)の中だけで完結します。
"""
import os
import stat
import subprocess
import sys
import tempfile
from datetime import datetime


# ---------------------------------------------------------------------------
# 1. subprocess.run() の基本
# ---------------------------------------------------------------------------
def section1_basic_subprocess_run():
    """subprocess.run() を使って外部コマンドを実行する、最も基本的な形。

    - command はシェルの文法(パイプ `|` やリダイレクト `>` など)を使わない、
      「コマンド名 + 引数」を並べた**リスト**で指定する。
    - capture_output=True を指定すると、標準出力・標準エラー出力が
      結果オブジェクトの .stdout / .stderr に文字列として格納される。
    - text=True を指定しないと、.stdout はバイト列(b"hello\\n"のような形)
      になってしまうので、文字列として扱いたいときは必ず指定する。
    - .returncode には終了コード(0なら正常終了)が入る。
    """
    result = subprocess.run(["echo", "hello from subprocess"], capture_output=True, text=True)
    print(f"  実行したコマンド: {result.args}")
    print(f"  returncode      : {result.returncode}")
    print(f"  stdout          : {result.stdout!r}")

    # 引数を複数渡すこともできる。シェルを経由しないので、引数はそのまま
    # 1つの値として渡される(スペースを含んでいても分割されない)。
    result2 = subprocess.run(
        ["echo", "サーバー監視スクリプトから", "こんにちは"],
        capture_output=True,
        text=True,
    )
    print(f"  stdout(複数引数): {result2.stdout!r}")


# ---------------------------------------------------------------------------
# 2. returncode を使ったエラーハンドリング
# ---------------------------------------------------------------------------
def section2_returncode_and_error_handling():
    """returncode を確認することで、例外を使わずにコマンドの成否を判定できる。

    サーバー運用スクリプトでは、コマンドが失敗しても Python プログラム
    自体は異常終了させず、「失敗した」という事実を記録して次の処理に
    進みたい場面が多い。subprocess.run() はデフォルトでは失敗しても
    例外を発生させず、returncode に結果を残すだけなので、この用途に
    向いている。
    """
    # sys.executable は「今実行しているpython3自身」へのパス。
    # 環境によって python3 コマンドの場所が違っても確実に動く。
    ok_result = subprocess.run(
        [sys.executable, "-c", "print('正常終了します'); exit(0)"],
        capture_output=True,
        text=True,
    )
    ng_result = subprocess.run(
        [sys.executable, "-c", "print('異常終了します'); exit(1)"],
        capture_output=True,
        text=True,
    )

    for label, result in [("成功するはずのコマンド", ok_result), ("失敗するはずのコマンド", ng_result)]:
        if result.returncode == 0:
            print(f"  [OK] {label}: returncode={result.returncode} -> 成功")
        else:
            print(f"  [NG] {label}: returncode={result.returncode} -> 失敗")

    # check=True を指定すると、returncodeが0以外のときに
    # CalledProcessError という例外を自動で発生させることもできる。
    # 「失敗したら即座に処理を止めたい」場面ではこちらが便利。
    try:
        subprocess.run([sys.executable, "-c", "exit(1)"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"  check=True の場合、失敗すると例外が発生する: {e}")


# ---------------------------------------------------------------------------
# 3. os.system() を使わない理由(シェルインジェクションの危険性)
# ---------------------------------------------------------------------------
def section3_why_not_os_system():
    """os.system() や shell=True を使うと、なぜ危険なのかを実際に確認する。

    os.system() は内部的に必ずシェル(bash など)を経由してコマンドを
    実行する。これは subprocess.run(..., shell=True) を使うのと同じ
    仕組みであり、コマンド文字列の中に外部から渡された値(ユーザー入力や
    設定ファイルの値など)をそのまま埋め込むと、「;」や「&&」のような
    シェルの特殊記号を使って、意図しない別のコマンドを実行されてしまう
    危険がある。これを「シェルインジェクション」と呼ぶ。

    ここでは実害のない echo コマンドだけを使って、その危険性を
    安全に体験する。
    """
    # 「外部から渡された値」を装った文字列(本来はユーザー入力や
    # 設定ファイルなどから来る可能性がある)
    untrusted_value = "hello; echo ATTACKER_INJECTED_COMMAND"

    # (A) 安全な書き方: リストで渡す(shell=Trueを使わない)
    #     この場合、untrusted_value は「1個の引数」としてそのまま
    #     echo に渡されるだけで、シェルによる解釈は一切行われない。
    safe_result = subprocess.run(["echo", untrusted_value], capture_output=True, text=True)
    print("  (A) 安全な書き方(リスト渡し・shell=Trueなし)の結果:")
    print(f"      stdout = {safe_result.stdout!r}")
    print("      -> 文字列がそのまま1つの引数として出力されるだけで、")
    print("         ';' 以降が別コマンドとして実行されることはない")

    # (B) 危険な書き方: 文字列を組み立てて shell=True で実行する
    #     (os.system() を使った場合も、内部的にはこれと同じことが起きる)
    #     untrusted_value の中の ';' がシェルによってコマンドの区切りと
    #     解釈され、2つのコマンドが実行されてしまう。
    dangerous_command = f"echo {untrusted_value}"
    dangerous_result = subprocess.run(dangerous_command, shell=True, capture_output=True, text=True)
    print("  (B) 危険な書き方(文字列 + shell=True)の結果:")
    print(f"      実行した文字列 = {dangerous_command!r}")
    print(f"      stdout = {dangerous_result.stdout!r}")
    print("      -> ';' が区切りとして解釈され、余計な2つ目のコマンドまで")
    print("         実行されてしまっている(今回はechoなので無害だが、")
    print("         これが 'rm -rf' のような破壊的なコマンドだったら重大事故になる)")
    print()
    print("  結論: os.system() は常にシェルを経由するため (B) と同じ危険がある。")
    print("        外部コマンドを実行するときは、os.system() ではなく")
    print("        subprocess.run(コマンドと引数のリスト) を使い、shell=True や")
    print("        文字列連結によるコマンド組み立てはできるだけ避けること。")


# ---------------------------------------------------------------------------
# 4. シバン行と実行権限を持つスクリプト
# ---------------------------------------------------------------------------
def section4_shebang_and_executable_script():
    """シバン行(#!/usr/bin/env python3)の役割を、実際にスクリプトを
    作って確認する。

    シバン行はスクリプトファイルの1行目に書く特別なコメントで、
    「このファイルをどのプログラムで実行すればよいか」をOSに伝える。
    `#!/usr/bin/env python3` は「PATHの中からpython3を探して、それで
    このファイルを実行してください」という意味になる(env経由にすることで、
    python3が /usr/bin/python3 でも /usr/local/bin/python3 でも動く)。

    シバン行があり、かつファイルに実行権限(chmod +x)が付いていれば、
    `python3 script.py` のように毎回python3を指定しなくても、
    `./script.py` や cron の設定ファイルの中でパスを直接書くだけで
    実行できるようになる。これはcronのようにOSが直接スクリプトを
    起動する仕組みと相性が良い。
    """
    script_body = (
        "#!/usr/bin/env python3\n"
        "# このファイル自体が、シバン行を持つ実行可能スクリプトの例\n"
        "print('シバン行のおかげで直接実行できました')\n"
    )

    tmp_dir = tempfile.mkdtemp(prefix="python_kiso_07_")
    script_path = os.path.join(tmp_dir, "healthcheck_demo.py")
    with open(script_path, "w", encoding="utf-8") as f:
        f.write(script_body)

    print(f"  作成したスクリプト: {script_path}")
    print("  --- スクリプトの中身 ---")
    for line in script_body.splitlines():
        print(f"  {line}")

    # 実行権限(chmod +x相当)を付与する。
    # 既存のパーミッションに「実行フラグ」を足す、というのが安全な作法。
    current_mode = os.stat(script_path).st_mode
    os.chmod(script_path, current_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    print("  -> os.chmod() で実行権限を付与しました(chmod +x 相当)")

    # シバン行 + 実行権限のおかげで、[python3, path] ではなく
    # [path] だけでスクリプトを実行できる。
    result = subprocess.run([script_path], capture_output=True, text=True)
    print(f"  ./healthcheck_demo.py 相当の実行結果: returncode={result.returncode}")
    print(f"  stdout: {result.stdout.strip()!r}")

    # 後片付け(この章の演習では一時ファイルを残さない方針を徹底する)
    os.remove(script_path)
    os.rmdir(tmp_dir)


# ---------------------------------------------------------------------------
# 5. cronでの定期実行を見越した、複数サービスのヘルスチェック
# ---------------------------------------------------------------------------
def run_command(command):
    """(演習1の模範解答と同じ考え方の)コマンド実行ヘルパー。"""
    result = subprocess.run(command, capture_output=True, text=True)
    return result.returncode, result.stdout


def parse_ping_output(ping_output):
    """(演習3の模範解答と同じ考え方の)ping出力の解析ヘルパー。"""
    return "0% packet loss" in ping_output


def section5_cron_style_health_check():
    """cronでの定期実行を見越した、複数サービスのヘルスチェックスクリプトの例。

    cronから起動されるスクリプトには、対話的なスクリプト(input()を使う
    など)とは違う設計上の注意点がある。

    - 人間が画面を見ているとは限らないので、input() のような
      対話的な処理は書かない(いつまでも待ち続けて固まってしまう)。
    - cronが渡すPATHなどの環境変数は、ログインシェルより少ないことが多い。
      コマンドやファイルは、できるだけ絶対パスで指定するのが安全。
    - 「正常に終わったか」を人間が毎回確認しに行くのではなく、
      returncode(終了コード)や、タイムスタンプ付きのログを残すことで、
      後から・あるいは別の監視ツールから自動的にチェックできるようにする。

    ここでは、複数の「サービス」を模したコマンドを実行し、
    タイムスタンプ付きのヘルスチェックレポートを組み立てる。
    """
    # 実際の運用では ["systemctl", "is-active", "nginx"] のような
    # コマンドになるが、ここでは環境に依存しない echo / python3 で代用する。
    services = {
        "web": ["echo", "web service is running"],
        "app": [sys.executable, "-c", "exit(0)"],
        "batch_job": [sys.executable, "-c", "exit(1)"],  # 失敗している想定
    }

    report = {}
    for service_name, command in services.items():
        returncode, _stdout = run_command(command)
        report[service_name] = returncode == 0

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"  [{timestamp}] ヘルスチェックレポート")
    for service_name, is_healthy in report.items():
        status = "OK" if is_healthy else "NG"
        print(f"  [{timestamp}] {service_name:<10}: {status}")

    unhealthy = [name for name, ok in report.items() if not ok]
    if unhealthy:
        print(f"  -> 異常のあるサービス: {', '.join(unhealthy)}(cronならここでアラート通知などにつなげる)")
    else:
        print("  -> すべてのサービスが正常です")

    # おまけ: pingコマンドの出力を模したテキストを解析する例
    fake_ping_output = "3 packets transmitted, 3 received, 0% packet loss, time 2004ms"
    reachable = parse_ping_output(fake_ping_output)
    print(f"  (参考) ping出力の解析結果: 到達可能 = {reachable}")


def main():
    print("=" * 70)
    print("1. subprocess.run() の基本")
    print("=" * 70)
    section1_basic_subprocess_run()

    print()
    print("=" * 70)
    print("2. returncode を使ったエラーハンドリング")
    print("=" * 70)
    section2_returncode_and_error_handling()

    print()
    print("=" * 70)
    print("3. os.system() を使わない理由(シェルインジェクションの危険性)")
    print("=" * 70)
    section3_why_not_os_system()

    print()
    print("=" * 70)
    print("4. シバン行と実行権限を持つスクリプト")
    print("=" * 70)
    section4_shebang_and_executable_script()

    print()
    print("=" * 70)
    print("5. cronでの定期実行を見越した、複数サービスのヘルスチェック")
    print("=" * 70)
    section5_cron_style_health_check()


if __name__ == "__main__":
    main()
