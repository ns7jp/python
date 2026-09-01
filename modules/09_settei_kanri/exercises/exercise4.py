"""演習4(応用): 複数環境(dev/staging/prod)向けの設定マージ(難易度: ★★★)"""


def build_environment_config(env_name, base_config, overrides):
    """環境名に応じて、共通設定を差分設定で上書きした新しい設定を作る。

    サーバーの設定は「開発環境(dev)」「ステージング環境(staging)」
    「本番環境(prod)」など、環境ごとに一部だけ値を変えたいことが
    よくあります(例: 本番だけログレベルをWARNINGにする、など)。

    この関数では、全環境で共通の設定 base_config をベースにして、
    overrides の中から env_name に対応する差分設定があれば、
    その差分でトップレベルのキーだけを上書きします
    (ネストした辞書の中身までは再帰的にマージしなくてよい「浅いマージ」)。

    仕様:
        - base_config はそのまま変更してはいけない(コピーしてから
          使うこと。呼び出し元の base_config が書き換わってしまうと、
          他の環境の設定を作るときに困るため)。
        - overrides は {"dev": {...}, "prod": {...}} のような、
          環境名をキーとする辞書。
        - overrides に env_name というキーがあれば、その中身の
          辞書を使って base_config のコピーのトップレベルキーを
          上書きする(新しいキーであれば追加する)。
        - overrides に env_name というキーがなければ、
          base_config のコピーをそのまま返す。
        - マージは「浅いマージ」でよい。つまり、値が辞書であっても
          その中身までは再帰的にマージせず、トップレベルのキー単位で
          そのまま置き換える。

    引数:
        env_name (str): "dev" や "staging" や "prod" などの環境名。
        base_config (dict): 全環境で共通のベース設定。
        overrides (dict): {環境名: {上書きしたい設定}} という形の辞書。

    戻り値:
        dict: base_config を env_name に対応する差分でマージした
              新しい辞書(base_config 自体は変更しない)。

    入出力例:
        >>> base = {"debug": True, "log_level": "INFO", "port": 8000}
        >>> overrides = {
        ...     "prod": {"debug": False, "log_level": "WARNING"},
        ... }
        >>> build_environment_config("prod", base, overrides)
        {'debug': False, 'log_level': 'WARNING', 'port': 8000}
        >>> build_environment_config("dev", base, overrides)
        {'debug': True, 'log_level': 'INFO', 'port': 8000}
        >>> base
        {'debug': True, 'log_level': 'INFO', 'port': 8000}
    """
    # TODO: base_config をコピーする(dict(base_config) や base_config.copy() など)
    # TODO: overrides に env_name があれば、そのキーと値でコピーを上書きする(update())
    # TODO: 上書き後の新しい辞書を返す(base_config自体は変更しないこと)
    raise NotImplementedError("build_environment_config を実装してください")
