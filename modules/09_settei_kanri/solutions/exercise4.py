"""演習4の模範解答: 複数環境(dev/staging/prod)向けの設定マージ"""


def build_environment_config(env_name, base_config, overrides):
    """環境名に応じて、共通設定を差分設定で上書きした新しい設定を作る。

    仕様の詳細は exercises/exercise4.py の docstring を参照してください。
    """
    # base_config を直接書き換えないよう、浅いコピーを作る
    merged = dict(base_config)

    # env_name に対応する差分設定があれば、それでトップレベルキーを上書きする
    if env_name in overrides:
        merged.update(overrides[env_name])

    return merged
