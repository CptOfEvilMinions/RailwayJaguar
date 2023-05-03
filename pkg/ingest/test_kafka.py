from pkg.ingest.kafka import CheckTopics
from typing import List


def test_checkTopics():
    ruleTopics: List[str] = [
        "zeek_conn",
        "zeek_dns",
        "zeek_files",
    ]
    kafkaTopics: List[str] = [
        "zeek_conn",
        "zeek_dns",
        "zeek_files",
    ]
    assert CheckTopics(kafkaTopics, ruleTopics) is None


def test_negativeCheckTopics():
    ruleTopics: List[str] = [
        "zeek_conn",
        "zeek_dns",
        "zeek_files",
    ]
    kafkaTopics: List[str] = [
        "zeek_dns",
        "zeek_files",
    ]
    assert CheckTopics(kafkaTopics, ruleTopics) is None