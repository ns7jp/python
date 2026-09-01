"""演習3: ディレクトリ内の.logファイル一覧をサイズ順に取得する

サーバーのディスク容量が逼迫してきたとき、まず確認したいのは
「どのログファイルが大きいのか」です。この演習では、pathlib.Path を使って
指定したディレクトリ直下の .log ファイルを調べ、サイズが大きい順に
並べ替えて一覧を作る処理を実装します。
"""

from pathlib import Path


def list_log_files_with_size(dir_path):
    """指定ディレクトリ直下にある拡張子 .log のファイルを、サイズの降順で一覧にする。

    pathlib.Path を使って実装すること。サブディレクトリの中は探索しない
    (指定したディレクトリの「直下」にあるファイルだけを対象にする)。
    .log 以外の拡張子のファイルは結果に含めない。

    引数:
        dir_path (str または pathlib.Path): 調べたいディレクトリのパス。

    戻り値:
        list[tuple[str, int]]: (ファイル名の文字列, サイズ(バイト, int)) の
            タプルを、サイズが大きい順(降順)に並べたリスト。
            .log ファイルが1つもない場合は空リスト [] を返す。

    入出力例:
        ディレクトリ /var/log/app の中に、次のファイルがあるとする。
            access.log  (100バイト)
            error.log   (300バイト)
            debug.log   (50バイト)
            notes.txt   (1000バイト、.log ではないので対象外)

        >>> list_log_files_with_size("/var/log/app")
        [('error.log', 300), ('access.log', 100), ('debug.log', 50)]

        >>> list_log_files_with_size("/path/to/empty_dir")
        []
    """
    # TODO: 1. dir_path を Path(dir_path) の形で pathlib.Path オブジェクトに変換する
    #          (すでに Path オブジェクトが渡された場合でも Path() で包んで問題ない)。
    # TODO: 2. dir_path.iterdir() でディレクトリ直下のエントリ(ファイルや
    #          サブディレクトリ)を1つずつ取り出す。
    # TODO: 3. 各エントリについて、entry.is_file() が True かつ
    #          entry.suffix == ".log" であるものだけを対象にする。
    # TODO: 4. 対象のファイルについて (entry.name, entry.stat().st_size) の
    #          タプルを作り、リストにまとめる。
    # TODO: 5. 集めたリストを、サイズ(タプルの2番目の要素)の降順で
    #          並べ替えて返す(sorted() の key引数と reverse=True を使う)。
    raise NotImplementedError("list_log_files_with_size を実装してください")
