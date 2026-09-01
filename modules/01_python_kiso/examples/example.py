"""
第1章 サンプルコード: 変数・データ型・演算子・f-string

このファイルは、サーバー運用でありそうな場面を想定しながら、
Pythonの基本(変数・データ型・演算子・f-string・round())の使い方を
実際に動かして確認するためのサンプルです。

実行方法:
    cd /home/user/python
    python3 modules/01_python_kiso/examples/example.py
"""

# ----------------------------------------------------------------------
# 1. 変数とデータ型
# ----------------------------------------------------------------------
print("=" * 60)
print("1. 変数とデータ型の確認")
print("=" * 60)

# サーバー名は文字列(str)で管理する
server_name = "web01"

# ディスクの使用容量・総容量はGB単位の数値(float)で管理する
disk_used_gb = 45.5
disk_total_gb = 100.0

# サーバーが「稼働中」かどうかは真偽値(bool)で管理できる
is_running = True

print(f"server_name の型: {type(server_name)} / 値: {server_name}")
print(f"disk_used_gb の型: {type(disk_used_gb)} / 値: {disk_used_gb}")
print(f"is_running の型: {type(is_running)} / 値: {is_running}")
print()


# ----------------------------------------------------------------------
# 2. 型変換(int() / float() / str())
# ----------------------------------------------------------------------
print("=" * 60)
print("2. 型変換の確認")
print("=" * 60)

# コマンド出力や設定ファイルから読み取った値は、たいてい文字列(str)で
# やってくる。計算するには数値に変換する必要がある。
port_str = "8080"
port_num = int(port_str)  # 文字列 -> 整数
print(f"文字列 \"{port_str}\" を int() で変換すると: {port_num} (型: {type(port_num)})")

usage_str = "45.5"
usage_num = float(usage_str)  # 文字列 -> 小数
print(f"文字列 \"{usage_str}\" を float() で変換すると: {usage_num} (型: {type(usage_num)})")

# 逆に、数値を文字列に変換してメッセージに組み込むこともよくある
count = 3
message = "接続中のクライアント数: " + str(count) + "台"
print(message)
print()


# ----------------------------------------------------------------------
# 3. 算術演算子で使用率を計算する(ディスク使用率の例)
# ----------------------------------------------------------------------
print("=" * 60)
print("3. ディスク使用率の計算")
print("=" * 60)

# 使用率(%) = 使用量 / 総量 * 100
disk_usage_percent = disk_used_gb / disk_total_gb * 100

# round() で小数点第2位までに丸める
disk_usage_percent_rounded = round(disk_usage_percent, 2)

print(f"ディスク使用量: {disk_used_gb}GB / 総容量: {disk_total_gb}GB")
print(f"丸める前の使用率: {disk_usage_percent}")
print(f"round()で丸めた使用率: {disk_usage_percent_rounded}")

# f-stringの書式指定 :.2f を使うと、丸め計算をしなくても
# 表示のときに小数点第2位まで揃えて見せることができる
print(f"f-stringで整形した表示: {server_name} のディスク使用率は {disk_usage_percent:.2f}% です")
print()


# ----------------------------------------------------------------------
# 4. 整数除算(//)と剰余(%)で稼働時間(uptime)を表示する
# ----------------------------------------------------------------------
print("=" * 60)
print("4. 稼働時間(uptime)の表示")
print("=" * 60)

# サーバーが起動してから経過した秒数(例: 93784秒)
uptime_seconds = 93784

# 1日 = 86400秒, 1時間 = 3600秒, 1分 = 60秒
days = uptime_seconds // 86400
remainder_after_days = uptime_seconds % 86400

hours = remainder_after_days // 3600
remainder_after_hours = remainder_after_days % 3600

minutes = remainder_after_hours // 60
seconds = remainder_after_hours % 60

print(f"稼働秒数 {uptime_seconds}秒 を分解すると:")
print(f"  {days}日 {hours}時間 {minutes}分 {seconds}秒")

if days > 0:
    uptime_text = f"{days}日{hours}時間{minutes}分{seconds}秒"
else:
    uptime_text = f"{hours}時間{minutes}分{seconds}秒"

print(f"人間が読みやすい形式: {uptime_text}")
print()


# ----------------------------------------------------------------------
# 5. 比較演算子・論理演算子でポート番号を検証する
# ----------------------------------------------------------------------
print("=" * 60)
print("5. ポート番号の検証")
print("=" * 60)

candidate_ports = [22, 8080, 70000, -1]

for port in candidate_ports:
    # 比較演算子(>=, <=)と論理演算子(and)を組み合わせて範囲チェックを行う
    is_valid = (port >= 0) and (port <= 65535)
    print(f"port={port} は妥当なポート番号か? -> {is_valid}")
print()


# ----------------------------------------------------------------------
# 6. メモリ使用率の閾値判定とアラートメッセージ
# ----------------------------------------------------------------------
print("=" * 60)
print("6. メモリ使用率のアラートメッセージ")
print("=" * 60)

memory_used_mb = 7200
memory_total_mb = 8000
threshold_percent = 80.0

memory_usage_percent = memory_used_mb / memory_total_mb * 100

# 比較演算子で閾値を超えているかどうかを判定する
if memory_usage_percent > threshold_percent:
    alert_message = f"警告: メモリ使用率が{memory_usage_percent:.2f}%です"
else:
    alert_message = f"正常: メモリ使用率は{memory_usage_percent:.2f}%です"

print(f"メモリ使用量: {memory_used_mb}MB / 総容量: {memory_total_mb}MB / 閾値: {threshold_percent}%")
print(alert_message)
print()

print("=" * 60)
print("サンプルコードの実行が完了しました。")
print("次は exercises/exercise1.py 〜 exercise4.py に挑戦してみましょう!")
print("=" * 60)
