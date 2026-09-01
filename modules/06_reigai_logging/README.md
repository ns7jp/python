# 第6章: 例外処理とロギング

## 1. 📘 この章で学ぶこと

プログラムを書いていると、必ずと言っていいほど「想定外のこと」が起こります。
ユーザーが数字のつもりで文字を入力してしまう、ネットワークが一時的に
つながらない、0で割り算をしてしまう……。こうした「エラー」が起きたときに
プログラムがいきなり止まってしまうと、サーバー運用の現場ではとても困った
ことになります。

この章では、そうした「想定外のこと」にあらかじめ備え、プログラムを
安全に動かし続けるための2つの技術を学びます。

- **例外処理**: エラーが起きても、プログラム全体を止めずに適切に対応する仕組み(`try`/`except`/`else`/`finally`)
- **ロギング**: 「いつ・何が起きたか」を記録として残し、後から調べられるようにする仕組み(`logging`モジュール)

具体的には、次のトピックを扱います。

- `try`/`except`/`else`/`finally` の基本
- 複数の`except`節(例外の種類ごとに処理を分ける)
- 独自例外クラス(`Exception`を継承したクラス)の定義
- `raise` で自分から例外を発生させる方法
- `logging`モジュールの基本(`getLogger`, `FileHandler`, `Formatter`, レベル設定)

「例外」も「ロギング」も、最初は少し取っつきにくく感じるかもしれません。
ですが、これらは実務のプログラムには欠かせない「安全に運用するための
知恵」です。落ち着いて、1つずつ手を動かしながら身につけていきましょう。💪

## 2. 🖥 サーバーエンジニアにとってなぜ重要か

サーバー構築・運用の現場では、「何かがおかしくなること」は日常茶飯事です。

- ディスクの空き容量が急になくなる
- 一部のサーバーだけネットワークが不安定になる
- 設定ファイルに想定外の値が書かれている
- 外部サービスへのリクエストがタイムアウトする

こうした異常事態が起きたときに、監視スクリプトや自動化ツールがそのまま
「エラーを出してプログラムごと停止」してしまうと、以下のような問題に
つながります。

- 本来チェックするはずだった残りのサーバーの確認が行われないままになる
- 障害に気づくのが遅れる(ツール自体が動いていないので通知も飛ばない)
- 深夜バッチなど、人が見ていない時間帯にツールが止まっていても誰も気づけない

**例外処理**を使うと、「起こりうる異常」をあらかじめ想定してキャッチし、
「1台のサーバーの確認に失敗しても、残りのサーバーは続けて確認する」
といった、堅牢(けんろう: 壊れにくく、安定していること)なツールを
作ることができます。

また、異常が起きたことを画面に一瞬表示するだけでは、後から
「昨日の夜中に何が起きていたのか」を調べることができません。
**ロギング**を使ってファイルに記録を残しておけば、障害調査(トラブル
シューティング)のときに、いつ・どのサーバーで・どんなエラーが
発生していたのかを時系列で追跡できます。実際の運用現場では、
`/var/log/` 以下にあるログファイルを調べることが障害対応の第一歩に
なることがほとんどです。「異常時にも動き続け、記録を残す」という
この章の内容は、インフラエンジニアの基本中の基本と言える技術です。

## 3. 📖 解説

### 3.1 例外とは何か

Pythonでは、プログラムの実行中に問題が起きると「例外(Exception)」という
特別なオブジェクトが発生し、通常の処理の流れが中断されます。
何も対策をしていないと、例外はそのままプログラムの外まで伝わり、
プログラムはエラーメッセージを表示して終了(異常終了)してしまいます。

```python
def divide(a, b):
    return a / b

divide(10, 0)
# ZeroDivisionError: division by zero
# (この行で処理が止まり、以降のコードは実行されない)
```

### 3.2 try/except の基本

`try`/`except` を使うと、例外が発生してもプログラムを止めずに、
自分で用意した対応処理を実行できます。

```python
try:
    result = 10 / 0
except ZeroDivisionError:
    print("0では割り算できません")
    result = None

print("この行は必ず実行される")
```

- `try:` の中に、例外が起きるかもしれない処理を書く
- 例外が発生すると、その時点で`try`節の残りは実行されず、対応する
  `except`節にジャンプする
- `except ZeroDivisionError:` のように、**どの種類の例外を捕まえるか**を
  指定する(何も指定しない`except:`は、あらゆる例外を捕まえてしまい
  意図しないバグまで隠してしまうため、基本的には避けるべき書き方です)

### 3.3 else と finally

`try`/`except` には、さらに `else` と `finally` という節を追加できます。

```python
try:
    value = int("42")
except ValueError:
    print("変換に失敗しました")
else:
    print(f"変換に成功しました: {value}")
finally:
    print("この処理は必ず実行されます")
```

- **`else`**: `try`節の中で例外が**発生しなかったとき**だけ実行される
  (「成功したときだけ行いたい処理」を書く場所)
- **`finally`**: 例外が発生してもしなくても、**必ず**最後に実行される
  (「ファイルを閉じる」「接続を切断する」など、後片付けの処理を
  書くのによく使われる)

実行される順番のイメージは次の通りです。

```
try節を実行
  ↓
例外が起きた場合                  例外が起きなかった場合
  ↓                                  ↓
対応するexcept節を実行           else節を実行
  ↓                                  ↓
        finally節を実行(どちらの場合も必ず実行される)
```

### 3.4 複数のexcept節

1つの`try`節の中で複数の種類の例外が起こりうる場合、`except`を複数
並べて、種類ごとに違う対応をすることができます。

```python
def convert_and_divide(value_str, divisor):
    try:
        number = int(value_str)
        return number / divisor
    except ValueError:
        print(f"'{value_str}' は整数に変換できません")
    except ZeroDivisionError:
        print(f"{divisor} で割ることはできません")
```

`except`節は**上から順番に**チェックされ、最初に一致した1つだけが
実行されます。より具体的な(範囲の狭い)例外を先に、より汎用的な
例外を後に書くのが基本です。

### 3.5 独自例外クラス(Exceptionを継承する)

`ValueError`や`ZeroDivisionError`はPythonが最初から用意している例外
ですが、自分のプログラム専用の例外クラスを作ることもできます。
やり方はとてもシンプルで、`Exception`クラスを継承したクラスを
定義するだけです。

```python
class ServerUnreachableError(Exception):
    """サーバーに到達できないことを表す独自例外。"""
    pass
```

独自例外クラスを使うと、「どんな種類の異常が起きたのか」をコードの
上で明確に表現できます。`except ServerUnreachableError:` と書けば、
「サーバーに到達できない」というこの種類の異常だけをピンポイントで
捕まえられ、それ以外の予期しないバグ(たとえばプログラム自体の
書き間違いなど)まで誤って握りつぶしてしまう事故を防げます。

### 3.6 raiseで自分から例外を発生させる

`raise`を使うと、自分から意図的に例外を発生させることができます。

```python
def check_server(is_reachable, name):
    if not is_reachable:
        raise ServerUnreachableError(f"サーバー{name}に到達できません")
    return f"サーバー{name}: 到達可能"
```

`raise 例外クラス(メッセージ)` という形で書きます。この`check_server`
関数を呼び出す側は、`try`/`except`を使ってこの例外を捕まえるか、
何もしなければそのまま呼び出し元の外まで例外が伝わっていきます。

### 3.7 loggingモジュールの基本

`print()`は画面に一時的に文字を表示するだけですが、`logging`モジュール
を使うと、「いつ・どのレベルの・どんな内容の記録か」をファイルなどに
残すことができます。

```python
import logging

# 1. ロガー(記録係)を名前付きで取得する
logger = logging.getLogger("server_monitor")

# 2. ロガー自体が処理する最低レベルを設定する
logger.setLevel(logging.INFO)

# 3. ログの出力先(ハンドラ)を作る。ここではファイルに出力するFileHandler
handler = logging.FileHandler("server_monitor.log")
handler.setLevel(logging.INFO)

# 4. ログの書式(フォーマット)を決める
formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
handler.setFormatter(formatter)

# 5. ハンドラをロガーに追加する
logger.addHandler(handler)

# これでログを記録できる
logger.info("サーバー監視を開始しました")
logger.warning("応答がやや遅いサーバーがあります")
logger.error("サーバーXへの接続に失敗しました")
```

**ログレベル**には、重大度の低い順に次のようなものがあります。

| レベル      | 用途の目安                                 |
|-------------|---------------------------------------------|
| `DEBUG`     | 開発中の詳細な調査用の情報                  |
| `INFO`      | 通常の動作記録(「処理を開始した」など)   |
| `WARNING`   | ただちに問題ではないが、注意が必要な事象   |
| `ERROR`     | 処理が失敗するなど、明確な問題              |
| `CRITICAL`  | プログラムの継続が困難なほど深刻な問題      |

`logger.setLevel(logging.INFO)` と設定すると、`INFO`未満のレベル
(つまり`DEBUG`)のログは記録されません。「開発中は`DEBUG`まで
細かく出す、本番運用では`INFO`以上だけ残す」といった調整ができるのが、
`print()`にはないloggingモジュールの大きな利点です。

(注意) `logging.getLogger(名前)` は、**同じ名前を指定すると同じ
ロガーオブジェクトを返す**という特徴があります。そのため、同じ名前で
ロガーを組み立てる関数を何度も呼び出すと、対策をしないとハンドラが
重複して追加されてしまい、1つのログメッセージが複数回ファイルに
書き込まれてしまいます。`if not logger.handlers:` のように、
「まだハンドラが設定されていない場合だけ追加する」という配慮が
重要です(この章の演習3で実際に扱います)。

### 3.8 例外処理とロギングの組み合わせ

実際の運用スクリプトでは、例外処理とロギングを組み合わせて使うことが
とても多いです。

```python
try:
    result = risky_operation()
except SomeError as e:
    logger.warning(f"処理に失敗しました: {e}")
    # ここでプログラムを止めずに、次の処理へ進める
```

このように、「エラーが起きても記録だけ残してプログラムは動き続ける」
という設計は、監視ツールや自動化バッチのような、長時間・繰り返し
動作するプログラムではとても重要な考え方です。

## 4. 💻 サンプルコードの説明

`examples/example.py` では、この章で学んだ内容をひとつずつ動かして
確認できます。

- **1. try/except/else/finallyの基本**: `read_config_value(config, key)`
  で、キーが存在する場合(`else`が実行される)と存在しない場合
  (`except`が実行される)の両方を試し、どちらの場合も`finally`が
  必ず実行されることを確認しています。
- **2. 複数のexcept節**: `convert_and_divide(value_str, divisor)` を、
  正常なケース・`ValueError`が起きるケース・`ZeroDivisionError`が
  起きるケースの3パターンで呼び出し、例外の種類ごとに違うメッセージが
  表示されることを確認しています。
- **3. 独自例外クラスとraise**: `DiskSpaceError`という独自例外クラスを
  定義し、`check_disk_usage(percent)`が閾値を超えたときに`raise`する
  様子と、それを`try`/`except`で捕まえる様子を確認しています。
- **4. loggingモジュールの基本**: `build_demo_logger(log_file_path)`で
  ロガーを組み立て、`DEBUG`/`INFO`/`WARNING`/`ERROR`の各レベルで
  ログを出力します。`DEBUG`のログはレベル設定により記録されないこと、
  それ以外はファイルに書き込まれることを、実際にファイルの中身を
  読み込んで表示することで確認しています。
- **5. 例外処理とロギングの組み合わせ**: `demo_retry_operation(...)`で、
  最初の数回はわざと失敗する処理を用意し、失敗するたびに
  `logger.warning(...)`で記録しながら再挑戦し、最終的に成功する
  様子を確認しています(演習4の内容の予告編です)。

実行方法は次の通りです。

```bash
cd /home/user/python
python3 modules/06_reigai_logging/examples/example.py
```

実行すると、各セクションの見出しとともに処理の流れが表示され、
最後にログファイルの中身も画面に表示されます。

## 5. ✍️ 演習問題

演習は `exercises/` フォルダの各ファイルにあります。関数の中身(TODO部分)を
実装してください。

### 演習1: `safe_divide` / `parse_int_safe` (難易度: ★☆☆)

- **ファイル**: `exercises/exercise1.py`
- **目的**: `try`/`except`の最も基本的な使い方(例外を捕まえて`None`を
  返す)を練習します。
- **ヒント**: `safe_divide`では`except ZeroDivisionError:`を、
  `parse_int_safe`では`except ValueError:`を使います。どちらも
  「`try`節で計算した値をそのまま`return`し、対応する`except`節では
  `None`を`return`する」という同じパターンです。

### 演習2: `ServerUnreachableError` / `check_server` / `check_server_safe` (難易度: ★★☆)

- **ファイル**: `exercises/exercise2.py`
- **目的**: `Exception`を継承した独自例外クラスの定義と、`raise`で
  例外を発生させる方法、そしてそれを`try`/`except`で捕まえて安全な
  戻り値に変換する方法を練習します。
- **ヒント**: `ServerUnreachableError`は`class ServerUnreachableError(Exception): pass`
  で定義できます。`check_server`では`if not is_reachable:`の中で
  `raise ServerUnreachableError(...)`を書きます。`check_server_safe`は
  `check_server`を`try`節の中で呼び出し、`except ServerUnreachableError:`
  でエラーメッセージの文字列を作って返します。

### 演習3: `setup_logger` (難易度: ★★☆)

- **ファイル**: `exercises/exercise3.py`
- **目的**: `logging`モジュールを使って、ファイルにログを出力する
  ロガーを組み立てる方法を練習します。ハンドラが重複して追加されない
  ようにする配慮も体験します。
- **ヒント**: `logging.getLogger(logger_name)`でロガーを取得し、
  `logger.setLevel(logging.INFO)`を設定します。`if not logger.handlers:`
  で「まだハンドラがなければ」という条件をつけ、その中で
  `logging.FileHandler(log_file_path)`を作り、`setLevel`と
  `setFormatter`を設定してから`logger.addHandler(handler)`します。
  最後に`logger`を`return`するのを忘れずに。

### 演習4(応用): `retry_with_logging` (難易度: ★★★)

- **ファイル**: `exercises/exercise4.py`
- **目的**: 例外処理とロギングを組み合わせ、「失敗を記録しながら
  再挑戦する」というリトライ処理を自分の手で実装します。
- **ヒント**: `for attempt in range(1, max_attempts + 1):`でループし、
  ループの中で`try: return func()`とします(成功したらそこで即座に
  `return`されるので、ループの続きは実行されません)。
  `except Exception as exc:`で失敗を捕まえ、`logger.warning(...)`で
  記録してから、その例外を変数(例: `last_error`)に保存します。
  ループが最後まで終わってしまった(＝すべて失敗した)場合は、
  ループを抜けたあとで`raise last_error`とします。

## 6. 🔍 進め方

1. `modules/06_reigai_logging/exercises/` の中の各ファイル
   (`exercise1.py` 〜 `exercise4.py`)を開き、`TODO` コメントと
   `raise NotImplementedError(...)` の部分を、docstringの仕様に沿って
   実装します。
2. 実装ができたら、リポジトリのルート(`/home/user/python`)で以下の
   コマンドを実行し、テストが通るか確認します。

   ```bash
   cd /home/user/python
   pytest modules/06_reigai_logging/tests
   ```

3. テストが赤色(FAILED)になったら、エラーメッセージを読んで
   実装を見直しましょう。エラーメッセージには「どの関数の」「どんな結果を
   期待していたか」がヒントとして書かれています。
4. すべてのテストが緑色(PASSED)になったら、その演習は完成です!
5. どうしても分からないときや、答え合わせをしたいときは
   `modules/06_reigai_logging/solutions/` フォルダにある模範解答を見て
   比べてみましょう。ただし、まずは自分の力で書いてみることを
   おすすめします。その方がずっと身につきます。

## 7. 🚀 発展課題

余裕がある人は、次の課題にもチャレンジしてみましょう。

- **発展1**: `parse_int_safe`を参考に、文字列を`float`に変換する
  `parse_float_safe(value)`という関数を自分で作ってみましょう
  (`ValueError`が起きたら`None`を返す、という同じ考え方です)。
- **発展2**: `ServerUnreachableError`にならって、
  `DiskFullError(Exception)`という独自例外クラスと、それを`raise`する
  `check_disk_space(free_percent)`という関数を自分で作ってみましょう
  (空き容量が10%未満なら`raise`する、など自由に設計してみてください)。
- **発展3**: `setup_logger`を改造し、ログの出力先をファイルだけでなく
  画面(コンソール)にも同時に出す `logging.StreamHandler` も
  追加してみましょう(`logger.addHandler`はハンドラをいくつでも
  追加できます)。
- **発展4**: `retry_with_logging`を改造し、「何回目の失敗か」だけでなく
  「合計で何秒待ってから再挑戦したか」もログに記録できるように
  してみましょう(`time.sleep(...)`を使って実際に待つ処理を
  入れてみるのも良い経験になります)。

## 8. ✅ この章のチェックリスト

- [ ] `try`/`except`の基本形を書き、例外が発生しても処理を継続できる
- [ ] `else`節と`finally`節が、それぞれどんなときに実行されるか説明できる
- [ ] 複数の`except`節を使って、例外の種類ごとに違う処理を書ける
- [ ] `Exception`を継承した独自例外クラスを定義できる
- [ ] `raise`を使って、自分から例外を発生させることができる
- [ ] `logging.getLogger`, `FileHandler`, `Formatter`を使って、
      ファイルにログを出力するロガーを組み立てられる
- [ ] ログレベル(DEBUG/INFO/WARNING/ERROR/CRITICAL)の意味と
      使い分けを説明できる
- [ ] 例外処理とロギングを組み合わせ、「失敗を記録しつつ処理を
      続ける(あるいは再挑戦する)」プログラムを書ける
- [ ] 4つの演習をすべて実装し、`pytest modules/06_reigai_logging/tests` が
      すべて合格することを確認した
