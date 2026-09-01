"""演習3のテスト: parse_ping_output

実際にpingコマンドを実行することはせず、pingコマンドが出力しそうな
テキストをその場で用意して解析する。外部ネットワークへのアクセスは
一切発生しない。
"""
from exercises.exercise3 import parse_ping_output

SUCCESS_OUTPUT = (
    "PING example.com (93.184.216.34): 56 data bytes\n"
    "64 bytes from 93.184.216.34: icmp_seq=0 ttl=56 time=12.3 ms\n"
    "64 bytes from 93.184.216.34: icmp_seq=1 ttl=56 time=11.9 ms\n"
    "\n"
    "--- example.com ping statistics ---\n"
    "3 packets transmitted, 3 received, 0% packet loss, time 2004ms\n"
)

FAILURE_OUTPUT = (
    "PING unreachable.example (10.0.0.99): 56 data bytes\n"
    "\n"
    "--- unreachable.example ping statistics ---\n"
    "3 packets transmitted, 0 received, 100% packet loss, time 2010ms\n"
)

PARTIAL_LOSS_OUTPUT = (
    "PING flaky.example (10.0.0.55): 56 data bytes\n"
    "64 bytes from 10.0.0.55: icmp_seq=0 ttl=56 time=12.3 ms\n"
    "\n"
    "--- flaky.example ping statistics ---\n"
    "3 packets transmitted, 2 received, 33% packet loss, time 2004ms\n"
)


def test_zero_percent_packet_loss_is_reachable():
    assert parse_ping_output(SUCCESS_OUTPUT) is True


def test_hundred_percent_packet_loss_matches_naive_substring_check():
    # 注意: この関数は "0% packet loss" という文字列が含まれるかどうかだけを
    # 見る、単純な(素朴な)実装です。そのため "100% packet loss" のように
    # 末尾がたまたま "0%" になっている文字列も、部分文字列としては
    # "0% packet loss" を含んでしまうため、True と判定されます。
    # これは仕様どおりの(意図された)単純な実装の挙動であり、本物の
    # pingコマンドの出力を厳密に解析したい場合は、正規表現などを使った
    # より厳密な判定が必要になります(7章の発展課題を参照)。
    assert parse_ping_output(FAILURE_OUTPUT) is True


def test_partial_packet_loss_is_not_reachable():
    assert parse_ping_output(PARTIAL_LOSS_OUTPUT) is False


def test_minimal_matching_string():
    assert parse_ping_output("...0% packet loss...") is True


def test_empty_string_is_not_reachable():
    assert parse_ping_output("") is False
