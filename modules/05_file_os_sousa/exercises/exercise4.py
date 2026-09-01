"""演習4(応用): 削除候補となる古いログファイルを一覧する

ログファイルを溜め込みすぎるとディスク容量を圧迫してしまうため、
「新しいものを一定数だけ残し、それより古いものは削除候補としてリストアップする」
というログローテーションの考え方は、運用の現場で定番の処理です。

この演習では、ディレクトリ内の .log ファイルを更新日時が新しい順に並べ、
「残す件数」を超えた分を削除候補として返す関数を実装します。

**重要: 安全のため、この関数は削除候補を一覧するだけで、実際にファイルを
削除する処理は絶対に行いません。** 実務でも、まず「消してよいものは何か」を
一覧・確認してから、別のステップで実際の削除を行う、という2段階に分けるのが
安全な設計です。
"""

from pathlib import Path


def find_old_log_candidates(dir_path, max_files_to_keep):
    """更新日時が新しい順に max_files_to_keep 件を残し、それ以外を削除候補として返す。

    指定ディレクトリ直下にある拡張子 .log のファイルを対象に、
    更新日時(st_mtime。ファイルの内容が最後に変更された日時)が
    新しいものから順に並べ替える。そのうち、上位 max_files_to_keep 件
    (＝残しておきたい新しいファイル)を除いた残りを「削除候補」として、
    ファイル名のリストで返す。

    **この関数は削除候補を一覧するだけの、安全設計の関数である。**
    関数の内部で os.remove() などの実際のファイル削除処理は一切行わない。
    削除候補を確認したうえで実際に削除するかどうかは、この関数の
    呼び出し側が判断すること。

    引数:
        dir_path (str または pathlib.Path): 調べたいディレクトリのパス。
        max_files_to_keep (int): 更新日時が新しい順に残しておきたい
            ファイルの件数。

    戻り値:
        list[str]: 削除候補となる .log ファイルの名前のリスト。
            更新日時が新しいものが上位 max_files_to_keep 件に含まれる場合、
            それらは結果に含まれない。.log ファイルの総数が
            max_files_to_keep 件以下の場合は、削除候補がないので
            空リスト [] を返す。

    入出力例:
        ディレクトリ /var/log/app の中に、更新日時が新しい順に
        app1.log, app2.log, app3.log, app4.log の4つがあるとする。

        >>> find_old_log_candidates("/var/log/app", max_files_to_keep=2)
        ['app3.log', 'app4.log']
        # 新しい2件(app1.log, app2.log)は残す対象なので削除候補に含まれない

        >>> find_old_log_candidates("/var/log/app", max_files_to_keep=10)
        []
        # ファイル数(4件)が残す件数(10件)以下なので、削除候補はなし
    """
    # TODO: 1. dir_path を Path(dir_path) の形で pathlib.Path オブジェクトに変換する。
    # TODO: 2. dir_path.iterdir() を使って、拡張子が .log のファイルだけを
    #          集めたリストを作る(演習3と同様に entry.is_file() と
    #          entry.suffix == ".log" で判定する)。
    # TODO: 3. 集めたファイルのリストを、entry.stat().st_mtime
    #          (更新日時、値が大きいほど新しい)の降順で並べ替える。
    # TODO: 4. 並べ替えた結果から、先頭の max_files_to_keep 件を除いた
    #          残り(スライス [max_files_to_keep:] が使える)を「削除候補」とする。
    # TODO: 5. 削除候補それぞれについて、ファイル名(entry.name)だけを
    #          集めたリストを作って返す。
    #          ※ 実際のファイル削除(os.remove など)は絶対に行わないこと。
    raise NotImplementedError("find_old_log_candidates を実装してください")
