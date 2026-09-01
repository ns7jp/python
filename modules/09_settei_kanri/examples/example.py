"""
09_settei_kanri / examples / example.py

この章のテーマ「設定ファイル管理(JSON / ini / 環境変数)」を
実際に動かして確認するためのサンプルスクリプトです。

実行方法:
    cd /home/user/python
    python3 modules/09_settei_kanri/examples/example.py

このスクリプトは外部ネットワークには一切アクセスしません。
サンプルの設定ファイルは実行のたびに一時ディレクトリ(tempfile)に
作成し、最後に自動的に削除します。
"""

import configparser
import json
import os
import tempfile


def section(title):
    """見出しを見やすく表示するための小さなヘルパー関数"""
    print()
    print("=" * 60)
    print(title)
    print("=" * 60)


# ---------------------------------------------------------------
# 1. JSON形式の設定ファイルを読み込む
# ---------------------------------------------------------------
def demo_json_config(work_dir):
    section("1. JSON設定ファイルの読み込み(json標準ライブラリ)")

    # まずはサンプルのJSON設定ファイルを用意する
    # (実際の現場では、このファイルは事前に用意されているものを読み込む)
    json_path = os.path.join(work_dir, "app_config.json")
    sample_data = {
        "app_name": "sample-web-app",
        "port": 8080,
        "debug": False,
        "allowed_hosts": ["localhost", "127.0.0.1"],
    }
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(sample_data, f, ensure_ascii=False, indent=2)

    print(f"作成したJSONファイル: {json_path}")

    # json.load() でファイルを開いたまま読み込み、Pythonの辞書として使う
    with open(json_path, "r", encoding="utf-8") as f:
        loaded = json.load(f)

    print("読み込んだ設定:", loaded)
    print("ポート番号だけ取り出す:", loaded["port"])

    # 存在しないファイルを読もうとするとどうなるか、も確認しておく
    missing_path = os.path.join(work_dir, "does_not_exist.json")
    if os.path.exists(missing_path):
        with open(missing_path, "r", encoding="utf-8") as f:
            missing_loaded = json.load(f)
    else:
        # 存在しない場合は空の辞書として扱う、というのはよくあるパターン
        missing_loaded = {}
    print("存在しないファイルの場合:", missing_loaded)


# ---------------------------------------------------------------
# 2. iniファイルの読み書き(configparser)
# ---------------------------------------------------------------
def demo_ini_config(work_dir):
    section("2. iniファイルの読み書き(configparserライブラリ)")

    ini_path = os.path.join(work_dir, "server.ini")

    # --- 書き込み ---
    writer = configparser.ConfigParser()
    writer["server"] = {"host": "0.0.0.0", "port": "8080"}
    writer["database"] = {"name": "sampledb", "user": "app_user"}

    with open(ini_path, "w", encoding="utf-8") as f:
        writer.write(f)

    print(f"作成したiniファイル: {ini_path}")
    with open(ini_path, "r", encoding="utf-8") as f:
        print("--- ファイルの中身 ---")
        print(f.read().rstrip())

    # --- 読み込み ---
    reader = configparser.ConfigParser()
    reader.read(ini_path, encoding="utf-8")

    print("\nセクション一覧:", reader.sections())

    # {セクション名: {キー: 値}} という入れ子の辞書に変換する
    as_dict = {
        section_name: dict(reader.items(section_name))
        for section_name in reader.sections()
    }
    print("入れ子の辞書に変換した結果:", as_dict)
    print("server.port の値(文字列であることに注意):", as_dict["server"]["port"])


# ---------------------------------------------------------------
# 3. 環境変数(os.environ / os.getenv)の基本
# ---------------------------------------------------------------
def demo_environment_variables():
    section("3. 環境変数の基本(os.environ / os.getenv)")

    # os.environ はOS全体の環境変数が入った辞書のようなオブジェクト。
    # ここではデモのために PYTHON_LESSON_DEMO_PORT という環境変数を
    # プログラムの中で一時的に設定してみる。
    os.environ["PYTHON_LESSON_DEMO_PORT"] = "9090"

    # 存在する環境変数を取得する
    port = os.getenv("PYTHON_LESSON_DEMO_PORT")
    print("PYTHON_LESSON_DEMO_PORT =", port)

    # 存在しない環境変数を取得しようとすると None が返る
    missing = os.getenv("PYTHON_LESSON_DEMO_NOT_SET")
    print("設定されていない環境変数 =", missing)

    # os.getenv の第2引数にはデフォルト値を指定できる
    missing_with_default = os.getenv("PYTHON_LESSON_DEMO_NOT_SET", "8000")
    print("デフォルト値つきで取得 =", missing_with_default)

    # 後片付け(デモ用に設定した環境変数を消しておく)
    del os.environ["PYTHON_LESSON_DEMO_PORT"]

    print(
        "\n※ 実際の現場では、環境変数はサーバー起動時にOS側や"
        "コンテナのenv設定で渡されることが多く、"
        "プログラム内で os.environ に代入することは基本的にありません。"
        "今回はデモのためにあえて代入しています。"
    )


# ---------------------------------------------------------------
# 4. 環境変数 > 設定ファイル > デフォルト値、という優先順位マージ
# ---------------------------------------------------------------
def demo_priority_merge():
    section("4. 環境変数・設定ファイル・デフォルト値の優先順位マージ")

    # 設定ファイルから読み込んだ想定のdict
    file_config = {"TIMEOUT": "30", "RETRY": "3"}

    # 環境変数を模した辞書(本物の os.environ の代わりにdictを使うと
    # テストがしやすくなる、という点は演習3でも扱います)
    fake_env = {"TIMEOUT": "10"}  # RETRY はここには無い、という状況

    def resolve(key, env, config, default):
        """env > config > default の優先順位で値を1つ選ぶ"""
        if key in env:
            return env[key]
        if key in config:
            return config[key]
        return default

    timeout = resolve("TIMEOUT", fake_env, file_config, "60")
    retry = resolve("RETRY", fake_env, file_config, "1")
    max_connections = resolve("MAX_CONNECTIONS", fake_env, file_config, "100")

    print("TIMEOUT         :", timeout, " (環境変数の値が優先された)")
    print("RETRY           :", retry, " (環境変数に無いので設定ファイルの値)")
    print("MAX_CONNECTIONS :", max_connections, " (どこにも無いのでデフォルト値)")

    print(
        "\nこのように「環境変数 > 設定ファイル > デフォルト値」という"
        "優先順位を決めておくと、開発時はデフォルト値のまま動かし、"
        "本番環境だけ環境変数で上書きする、といった柔軟な運用ができます。"
    )


# ---------------------------------------------------------------
# 5. 複数環境(dev/staging/prod)向け設定の切り替え
# ---------------------------------------------------------------
def demo_multi_environment():
    section("5. dev/staging/prod など複数環境向けの設定切り替え")

    # 全環境で共通のベース設定
    base_config = {
        "app_name": "sample-web-app",
        "debug": True,
        "log_level": "DEBUG",
        "worker_count": 1,
    }

    # 環境ごとの差分設定(トップレベルのキーだけ上書きする「浅いマージ」)
    overrides = {
        "dev": {},  # devはbase_configのままでよいので差分なし
        "staging": {"log_level": "INFO", "worker_count": 2},
        "prod": {"debug": False, "log_level": "WARNING", "worker_count": 4},
    }

    def build_config(env_name, base, env_overrides):
        merged = dict(base)  # base_config自体は書き換えないようコピーする
        if env_name in env_overrides:
            merged.update(env_overrides[env_name])
        return merged

    for env_name in ["dev", "staging", "prod"]:
        merged = build_config(env_name, base_config, overrides)
        print(f"[{env_name}] {merged}")

    print("\nベース設定は変更されていないことも確認:")
    print("base_config =", base_config)


# ---------------------------------------------------------------
# 6. (参考) PyYAML でYAML形式の設定を読み込む
# ---------------------------------------------------------------
def demo_yaml_config():
    section("6. (参考) PyYAMLでYAML形式の設定を読み込む")

    try:
        import yaml
    except ImportError:
        print("pyyaml がインストールされていないため、このデモはスキップします。")
        return

    # YAMLはインデントで構造を表す設定ファイル形式。JSONより人間が読み書き
    # しやすいため、docker-composeやKubernetesなどでもよく使われる。
    yaml_text = """
    server:
      host: 0.0.0.0
      port: 8080
    features:
      - logging
      - metrics
    """
    loaded = yaml.safe_load(yaml_text)
    print("YAML文字列から読み込んだ設定:", loaded)
    print("server.port の値:", loaded["server"]["port"])


# ---------------------------------------------------------------
# 7. 機密情報はハードコードしない、という注意点
# ---------------------------------------------------------------
def demo_secret_handling():
    section("7. 機密情報(パスワードなど)はソースコードに書かない")

    # 悪い例(あくまでコメントで示すだけで、実際にはこう書かない):
    #     DB_PASSWORD = "s3cr3t-password"  # NG! ソースコードに直書き
    #
    # 良い例: 環境変数から読み込む。環境変数が無い場合の挙動も
    # あらかじめ決めておく(ここではエラーにする例を示す)。
    db_password = os.getenv("DEMO_DB_PASSWORD")
    if db_password is None:
        print(
            "DEMO_DB_PASSWORD が設定されていません"
            "(本番のコードではここで起動を中止するのが安全です)"
        )
    else:
        # パスワードそのものをログに出力しないよう、マスクして表示する
        print("DEMO_DB_PASSWORD が設定されています: " + "*" * len(db_password))


def main():
    # このスクリプト専用の一時ディレクトリを作り、終わったら自動で削除する
    with tempfile.TemporaryDirectory(prefix="settei_kanri_demo_") as work_dir:
        demo_json_config(work_dir)
        demo_ini_config(work_dir)

    demo_environment_variables()
    demo_priority_merge()
    demo_multi_environment()
    demo_yaml_config()
    demo_secret_handling()

    section("完了")
    print("すべてのデモが正常に実行されました。")


if __name__ == "__main__":
    main()
