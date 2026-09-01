"""演習4の模範解答: 複数サービスのヘルスチェックレポートを作る

仕様の詳細はexercises/exercise4.pyのdocstringを参照してください。
"""
import subprocess


def build_health_check_script_report(commands):
    """複数サービスのコマンドを実行し、サービスごとの成功/失敗をまとめる。

    仕様はexercises/exercise4.pyのdocstringを参照。
    """
    report = {}
    for service_name, command in commands.items():
        result = subprocess.run(command, capture_output=True, text=True)
        report[service_name] = result.returncode == 0
    return report
