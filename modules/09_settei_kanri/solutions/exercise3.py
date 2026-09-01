"""演習3の模範解答: 環境変数・設定ファイル・デフォルト値の優先順位マージ"""


def resolve_setting(key, env, config, default):
    """優先順位に従って設定値を1つに決定する。

    仕様の詳細は exercises/exercise3.py の docstring を参照してください。
    優先順位: env > config > default
    """
    if key in env:
        return env[key]

    if key in config:
        return config[key]

    return default
