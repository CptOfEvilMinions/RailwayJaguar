from typing import Dict, Any, List
from cli.yaml_checker import (
    REQUIRED_KEYS,
    check_required_fields,
    check_version,
    check_kind,
    check_python_rule,
    check_kafka_topic,
    check_tests,
)

def test_check_kind():
    assert check_kind("stream_alert") is True


def test_negative_check_kind():
    assert check_kind("alert") is False


def test_check_version():
    assert check_version("v1") is True


def test_negative_check_version():
    assert check_version("1") is False


def test_check_required_fields():
    assert check_required_fields(REQUIRED_KEYS) is True
    REQUIRED_KEYS.add("MITRE ATT&CK")
    REQUIRED_KEYS.add("foo")
    REQUIRED_KEYS.add("bar")
    assert check_required_fields(REQUIRED_KEYS) is True


def test_negative_check_required_fields():
    assert check_required_fields({"hello"}) is False


def test_check_python_rule():
    assert check_python_rule("hello.py") is True


def test_negative_check_python_rule():
    assert check_python_rule("hello.c") is False


def test_check_kafka_topic():
    assert check_kafka_topic("hello") is True


def test_negative_check_kafka_topic():
    assert check_kafka_topic("foor bar") is False


def test_check_tests():
    tests: List[Dict[str, Any]] = [
        {
            "name": "True positive",
            "result": True,
            "event": {
                "ts": 1644692340.170364,
                "uid": "CY6M3z4XaPqkC7ZPdc",
                "id.orig_h": "172.16.50.100",
                "id.orig_p": 65459,
            }
        }
    ]
    assert check_tests(tests) is True