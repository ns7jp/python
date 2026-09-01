# 第8章: ネットワークとAPI連携

## 1. 📘 この章で学ぶこと

サーバー構築エンジニア(インフラエンジニア)の仕事では、「あのサーバーは
ちゃんと動いているか?」「監視サービスのAPIから最新の状態を取得したい」
といった、ネットワーク越しのやり取りが欠かせません。この章では、Pythonで
ネットワーク通信を扱うための基本を学びます。

- **socketモジュールの基礎**: TCP接続の考え方と、指定したホスト・
  ポートに接続できるかどうかを調べる方法(ポート疎通確認)
- **requestsライブラリでのHTTP通信**: WebサーバーやAPIにGET
  リクエストを送り、レスポンス(応答)を受け取る方法
- **json.loads / json.dumps**: サーバーやAPIとやり取りされる
  JSON形式のデータを、Pythonの辞書(dict)と相互に変換する方法
- **依存性注入(いそんせいちゅうにゅう)**: 通信を行う処理を関数の
  外から差し替えられるようにする設計。テストのしやすさに直結する
  重要な考え方です
- **unittest.mockによるモック**: 本物のネットワーク通信を行わずに、
  「通信が成功したとき」「失敗したとき」の動作を再現してテストする方法

具体的には、次のトピックを扱います。

- `socket.create_connection`でのTCP接続確認
- `requests.get`によるHTTP GETリクエストとステータスコードの取得
- `json.loads`(JSON文字列 → 辞書)と`json.dumps`(辞書 → JSON文字列)
- 関数の引数として通信処理を渡す「依存性注入」パターン
- `unittest.mock.patch`を使ったモック化
- `socket`モジュールで簡易サーバー(エコーサーバー)を自分で実装する方法

「ネットワーク」と聞くと難しそうに感じるかもしれませんが、この章の
演習はすべて**自分のパソコンの中だけ**で完結します。外部のインター
ネットには一切接続しないので、安心して手を動かしてみてください。🌐

## 2. 🖥 サーバーエンジニアにとってなぜ重要か

サーバー構築・運用の現場では、「ネットワーク越しに何かを確認する」
仕事が数えきれないほどあります。

- **ポート疎通確認**: 「Webサーバーの80番ポートは開いているか?」
  「新しく立てたサーバーの22番ポート(SSH)に接続できるか?」を
  確認するのは、サーバー構築・障害調査の基本中の基本です。手動で
  `telnet`や`nc`コマンドを打つこともできますが、これをPythonで
  自動化できれば、何十台ものサーバーを一括でチェックするツールを
  自分で作れるようになります。
- **外部API・監視サービスとの連携**: 多くの監視ツール(Datadog、
  Mackerel、Prometheusなど)は、HTTP経由でAPIを公開しています。
  「サーバーの状態を取得する」「アラートを送信する」といった
  操作をPythonから自動で行うには、`requests`ライブラリでのHTTP
  通信の基本を押さえておく必要があります。
- **JSON形式のレスポンス解析**: 現代のほとんどのAPIは、結果を
  JSON形式で返します。取得したJSONから必要な情報(CPU使用率、
  メモリ使用率、ステータスなど)だけを取り出して活用する力は、
  監視ツールや自動化スクリプトを作る上で欠かせません。
- **テストしやすい設計(依存性注入・モック)**: 実際の運用スクリプト
  は、本物のサーバーやAPIに接続しないとテストできないようでは
  困ります。「通信処理を外から差し替えられるようにする」
  「`unittest.mock`で通信結果を再現する」といった設計・技術を
  身につけることで、**安全かつ高速に**、何度でもテストを実行できる
  ツールを作れるようになります。これはインフラエンジニアに限らず、
  ソフトウェア開発全般で重宝されるスキルです。

この章で学ぶ内容は、「サーバー監視ツール」や「複数サーバーへの
一括ヘルスチェックツール」といった、インフラエンジニアが実務で
よく作ることになるプログラムの土台そのものです。

## 3. 📖 解説

### 3.1 socketモジュールとTCP接続の基本

`socket`モジュールは、Pythonでネットワーク通信を行うための標準
ライブラリです。TCP(Transmission Control Protocol)は、
「相手と接続を確立してからデータをやり取りする」通信方式で、
Webサーバー(HTTP)やSSH、データベースへの接続など、多くの
サーバーサービスがTCPの上で動いています。

「あるホストのあるポートに接続できるか」を調べるだけであれば、
`socket.create_connection`が便利です。

```python
import socket

try:
    with socket.create_connection(("127.0.0.1", 22), timeout=1.0) as conn:
        print("接続できました(SSHサーバーが起動している可能性が高い)")
except OSError:
    print("接続できませんでした(サーバーが起動していない、ポートが閉じている、など)")
```

- `("127.0.0.1", 22)`のように、接続先を`(ホスト, ポート)`のタプルで
  指定する
- `timeout`を指定しておくと、応答がないサーバーにいつまでも
  待たされることを防げる
- 接続に失敗すると、`ConnectionRefusedError`や`socket.timeout`
  (`TimeoutError`)といった例外が発生する。これらはすべて
  `OSError`の派生クラスなので、`except OSError:`でまとめて
  捕まえられる

### 3.2 requestsライブラリでのHTTP通信

`requests`は、Pythonで最もよく使われるHTTP通信用の外部ライブラリ
です。標準ライブラリではありませんが、この教材ではインストール
済みのものとして使用します。

```python
import requests

response = requests.get("https://example.com/api/status")
print(response.status_code)  # 200, 404, 500 などのHTTPステータスコード
print(response.text)         # レスポンスの本文(文字列)
```

- `requests.get(url)`でGETリクエストを送信する
- 戻り値は`Response`オブジェクトで、`.status_code`(ステータス
  コード)や`.text`(本文の文字列)、`.json()`(本文をJSONとして
  パースした結果)などの属性・メソッドを持つ
- ネットワークが不安定な場合や、相手サーバーが応答しない場合には
  例外(`requests.exceptions.RequestException`とその派生クラス)が
  発生することがある

(注意) この章の演習・サンプルコードでは、実際に`requests.get`で
外部サイトに接続することは一切ありません。次の3.3・3.4で説明する
「依存性注入」や「モック」を使って、通信結果を安全に再現します。

### 3.3 依存性注入(いそんせいちゅうにゅう)という考え方

「依存性注入(Dependency Injection、略してDI)」とは、関数や
クラスが内部で使う処理を、**外から渡せるようにしておく**設計の
ことです。言葉は難しそうですが、やっていることはシンプルです。

```python
import requests

# 依存性注入をしていない例(常にrequests.getが直接呼ばれる)
def check_status_bad(url):
    response = requests.get(url)
    return response.status_code


# 依存性注入をした例(http_get引数で通信処理を差し替えられる)
def check_status_good(url, http_get=None):
    getter = http_get if http_get is not None else requests.get
    response = getter(url)
    return response.status_code
```

`check_status_bad`は、テストしようとすると必ず本物のネットワーク
通信が発生してしまいます。一方`check_status_good`は、テストの
ときには`http_get`引数に「本物そっくりのダミー関数」を渡すことで、
外部通信なしで動作を確認できます。

```python
class FakeResponse:
    status_code = 200

def fake_get(url):
    return FakeResponse()

# 本物のネットワーク通信は一切発生しない
result = check_status_good("http://example.com", http_get=fake_get)
print(result)  # 200
```

このように「外部から差し替え可能にしておく」ことで、プログラムは
**テストしやすく(テスタブルに)**なります。これは実務のプログラム
設計でとても重視される考え方です。

### 3.4 unittest.mockによるモック

依存性注入のために毎回引数を追加する代わりに、Python標準
ライブラリの`unittest.mock`を使うと、既存の関数やオブジェクトを
**一時的に**別のもの(モック)に差し替えることができます。

```python
from unittest.mock import patch
import requests

class FakeResponse:
    status_code = 200

with patch("requests.get") as mock_get:
    mock_get.return_value = FakeResponse()
    response = requests.get("http://example.com")  # 実際には通信しない
    print(response.status_code)  # 200
    print(mock_get.call_count)   # 1(1回呼ばれたことが分かる)
```

- `patch("対象のパス")`で、指定した名前の関数・オブジェクトを
  一時的に置き換える(`with`ブロックを抜けると元に戻る)
- `mock_get.return_value = ...`で、モックが呼ばれたときに返す
  値を指定できる
- `mock_get.call_count`や`mock_get.call_args`など、モックが
  「何回」「どんな引数で」呼ばれたかを後から確認することもできる

依存性注入と`unittest.mock`は、どちらも「本物の通信を行わずに
テストする」という同じ目的のための、それぞれ違ったアプローチ
です。この章の演習2では主に依存性注入(`http_get`引数)を扱い、
サンプルコードではあわせて`unittest.mock.patch`の使い方も紹介
します。

### 3.5 json.loads / json.dumps

JSON(JavaScript Object Notation)は、多くのWeb APIで使われる
データ形式です。Python標準ライブラリの`json`モジュールを使うと、
JSON文字列とPythonの辞書・リストを簡単に相互変換できます。

```python
import json

# 辞書 -> JSON文字列(APIにデータを送るときなど)
data = {"host": "web01", "cpu": 42}
json_text = json.dumps(data, ensure_ascii=False)
print(json_text)  # {"host": "web01", "cpu": 42}

# JSON文字列 -> 辞書(APIから返ってきたデータを読み取るときなど)
parsed = json.loads(json_text)
print(parsed["cpu"])  # 42
```

- `json.dumps(辞書)`: Pythonのオブジェクトを**JSON文字列**に変換する
  (dump = 書き出す、s = string)
- `json.loads(文字列)`: JSON文字列を**Pythonのオブジェクト**(主に
  辞書やリスト)に変換する(load = 読み込む、s = string)
- `ensure_ascii=False`を指定すると、日本語などの非ASCII文字が
  `\uXXXX`形式にエスケープされず、そのまま出力される

通信相手から返ってくるデータは、必ずしも期待通りの形をしている
とは限りません。壊れたJSON文字列を渡すと`json.JSONDecodeError`
という例外が発生するため、実務のコードでは`try`/`except`で
このケースに備えることがとても重要です。

```python
try:
    data = json.loads("これはJSONではありません")
except json.JSONDecodeError:
    print("JSONの解析に失敗しました")
    data = {}
```

## 4. 💻 サンプルコードの説明

`examples/example.py` では、この章で学んだ内容をひとつずつ動かして
確認できます。

- **1. ポート疎通確認**: 自分のマシン上(127.0.0.1)に一時的な
  ソケットサーバーを立て、`is_port_open`でそのポートに接続できる
  ことを確認します。その後サーバーを閉じ、同じポートには接続
  できなくなる(`False`が返る)様子も確認します。
- **2-a. 依存性注入によるHTTP通信の確認**: `check_http_status`
  関数に、正常応答(200)・エラー応答(500)・通信失敗(タイムアウト)
  の3パターンのダミー関数を`http_get`引数として渡し、それぞれの
  戻り値がどう変わるかを確認します。
- **2-b. unittest.mock.patchの利用**: `requests.get`自体を
  `unittest.mock.patch`で一時的に差し替え、`http_get`引数を
  渡さない場合でも外部通信なしで動作を確認できることを見ます。
  モックが呼ばれた回数(`call_count`)も表示します。
- **3. json.loads / json.dumps**: 辞書をJSON文字列に変換する例と、
  正常なJSON・壊れたJSONそれぞれを`parse_server_status_json`で
  パースした結果を確認します。
- **4. 簡易エコーサーバー**: 空いているポートを動的に取得し、
  `start_echo_server`を別スレッド(`daemon=True`)で起動したあと、
  `send_echo_message`でメッセージを送信し、送った内容がそのまま
  返ってくることを確認します。

実行方法は次の通りです。

```bash
cd /home/user/python
python3 modules/08_network_api/examples/example.py
```

実行すると、各セクションの見出しとともに、ポート確認・HTTP通信
(ダミー)・JSON解析・エコーサーバーそれぞれの動作結果が表示されます。

## 5. ✍️ 演習問題

演習は `exercises/` フォルダの各ファイルにあります。関数の中身(TODO部分)を
実装してください。

### 演習1: `is_port_open` (難易度: ★★☆)

- **ファイル**: `exercises/exercise1.py`
- **目的**: `socket.create_connection`を使ったTCP接続確認と、接続
  失敗時の例外処理(`OSError`)を練習します。
- **ヒント**: `try`節の中で`socket.create_connection((host, port),
  timeout=timeout)`を`with`文と組み合わせて呼び出し、成功したら
  `True`を返します。`except OSError:`で`False`を返せば、
  `ConnectionRefusedError`や`socket.timeout`もまとめて捕まえられます。

### 演習2: `check_http_status` (難易度: ★★☆)

- **ファイル**: `exercises/exercise2.py`
- **目的**: `requests.get`によるHTTP通信と、テストしやすくする
  ための「依存性注入」の設計を練習します。
- **ヒント**: `http_get`引数が`None`でなければそれを、`None`で
  あれば`requests.get`を使う、という条件分岐(`getter = http_get
  if http_get is not None else requests.get`)がポイントです。
  `try`/`except Exception:`で通信中の例外をまとめて`None`に
  変換します。

### 演習3: `parse_server_status_json` (難易度: ★☆☆)

- **ファイル**: `exercises/exercise3.py`
- **目的**: `json.loads`によるJSON文字列の解析と、辞書内包表記
  (dict comprehension)を使ったキーの絞り込みを練習します。
- **ヒント**: `try`節で`json.loads(json_text)`を呼び出し、
  `json.JSONDecodeError`が起きたら`except`節で`{}`を返します。
  パース結果が辞書かどうかは`isinstance(data, dict)`で確認できます。
  最後は`{key: data[key] for key in ("status", "cpu", "memory") if
  key in data}`のような辞書内包表記でまとめると簡潔に書けます。

### 演習4(応用): `start_echo_server` / `send_echo_message` (難易度: ★★★)

- **ファイル**: `exercises/exercise4.py`
- **目的**: `socket`モジュールを使い、サーバー側(待ち受け)と
  クライアント側(接続)の両方を自分の手で実装します。
- **ヒント**: `start_echo_server`は、
  「ソケットを作る→`bind`する→`listen`する→`accept`で1接続
  受け付ける→`recv`で受信→`sendall`で送り返す→閉じる」という
  流れです。`send_echo_message`は、
  「ソケットを作る→`connect`する→`sendall`で送信→`recv`で
  受信→デコードして返す」という流れです。この2つの関数は
  それぞれ別のプロセス(あるいは別スレッド)で動くことを
  イメージしながら実装してみましょう。

## 6. 🔍 進め方

1. `modules/08_network_api/exercises/` の中の各ファイル
   (`exercise1.py` 〜 `exercise4.py`)を開き、`TODO` コメントと
   `raise NotImplementedError(...)` の部分を、docstringの仕様に沿って
   実装します。
2. 実装ができたら、リポジトリのルート(`/home/user/python`)で以下の
   コマンドを実行し、テストが通るか確認します。

   ```bash
   cd /home/user/python
   pytest modules/08_network_api/tests
   ```

3. テストが赤色(FAILED)になったら、エラーメッセージを読んで
   実装を見直しましょう。エラーメッセージには「どの関数の」「どんな結果を
   期待していたか」がヒントとして書かれています。
4. すべてのテストが緑色(PASSED)になったら、その演習は完成です!
5. どうしても分からないときや、答え合わせをしたいときは
   `modules/08_network_api/solutions/` フォルダにある模範解答を見て
   比べてみましょう。ただし、まずは自分の力で書いてみることを
   おすすめします。その方がずっと身につきます。

## 7. 🚀 発展課題

余裕がある人は、次の課題にもチャレンジしてみましょう。

- **発展1**: `is_port_open`を使って、複数のポート番号
  (例: `[22, 80, 443, 8080]`)をまとめてチェックし、「開いている
  ポートの一覧」を返す`scan_ports(host, ports)`という関数を
  自分で作ってみましょう。
- **発展2**: `check_http_status`を参考に、レスポンスの本文
  (`.text`や`.json()`)も一緒に取得できるように改造した
  `fetch_json(url, http_get=None)`という関数を作ってみましょう
  (取得できなかった場合は`None`を返す、など自由に設計してみて
  ください)。
- **発展3**: `parse_server_status_json`を改造し、"cpu"や"memory"の
  値が90以上だった場合に`"警告"`という文字列を含む結果を返すよう
  にした`evaluate_server_status(json_text)`という関数を作って
  みましょう。
- **発展4**: `start_echo_server`を改造し、受け取ったメッセージを
  そのまま返すのではなく、`.upper()`で大文字に変換してから返す
  `start_uppercase_server(host, port)`を作ってみましょう(演習4の
  `send_echo_message`はそのまま流用できます)。

## 8. ✅ この章のチェックリスト

- [ ] `socket.create_connection`を使って、TCP接続の成功・失敗を
      判定できる
- [ ] ポート確認のテストでは、外部の実サーバーではなく
      127.0.0.1上の自作サーバーや動的に取得したポート番号を使う
      理由を説明できる
- [ ] `requests.get`でHTTP GETリクエストを送り、
      `.status_code`でステータスコードを取得できる
- [ ] 「依存性注入」とは何か、なぜテストしやすくなるのかを
      自分の言葉で説明できる
- [ ] `unittest.mock.patch`を使って、関数やオブジェクトを一時的に
      差し替えられる
- [ ] `json.loads`でJSON文字列を辞書に変換し、`json.dumps`で
      辞書をJSON文字列に変換できる
- [ ] 壊れたJSON文字列を`json.JSONDecodeError`で捕まえ、安全な
      戻り値(空の辞書など)に変換できる
- [ ] `socket`モジュールを使って、簡単な待ち受けサーバー
      (`bind`/`listen`/`accept`)とクライアント(`connect`/`send`/
      `recv`)の両方を実装できる
- [ ] 4つの演習をすべて実装し、`pytest modules/08_network_api/tests` が
      すべて合格することを確認した
