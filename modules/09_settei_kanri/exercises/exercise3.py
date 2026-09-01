"""演習3: 環境変数・設定ファイル・デフォルト値の優先順位マージ(難易度: ★★☆)"""


def resolve_setting(key, env, config, default):
    """優先順位に従って設定値を1つに決定する。

    実際のサーバー運用では、同じ設定項目(例: ポート番号)が
    「環境変数」「設定ファイル」「プログラム内のデフォルト値」の
    複数の場所で指定できることがよくあります。
    その場合、一般的には次の優先順位で値を決定します。

        1. 環境変数(env)に key があれば、その値を最優先で使う
        2. 環境変数になければ、設定ファイル(config)に key があれば
           その値を使う
        3. どちらにもなければ、デフォルト値(default)を使う

    この関数では、本物の os.environ の代わりに env という辞書を
    引数として受け取ります(テストしやすくするためです)。

    仕様:
        - env に key が存在すれば env[key] を返す。
        - env に key が存在せず、config に key が存在すれば
          config[key] を返す。
        - env にも config にも key が存在しなければ default を返す。

    引数:
        key (str): 取得したい設定項目の名前。
        env (dict): 環境変数を模した辞書。
        config (dict): 設定ファイルの中身を模した辞書。
        default: env にも config にも key がない場合に使う値。

    戻り値:
        env, config, default のいずれか、優先順位に従って
        選ばれた値。

    入出力例:
        >>> resolve_setting("PORT", {"PORT": "9000"}, {"PORT": "8080"}, 80)
        '9000'

        >>> resolve_setting("PORT", {}, {"PORT": "8080"}, 80)
        '8080'

        >>> resolve_setting("PORT", {}, {}, 80)
        80
    """
    # TODO: env に key があれば env[key] を返す
    # TODO: なければ config に key があれば config[key] を返す
    # TODO: どちらにもなければ default を返す
    raise NotImplementedError("resolve_setting を実装してください")
