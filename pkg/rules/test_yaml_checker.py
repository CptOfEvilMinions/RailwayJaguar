from pkg.rules.yaml_checker import (
    validateVersion,
    validateKind,
    validatePythonRule,
    validateKafkaTopic,
    kafkaTopicRegex,
    pythonFilePathRegex,
)
import pytest


def test_validateKind():
    assert validateKind("stream_alert") is True


def test_negative_validateKind():
    assert validateKind("alert") is False


def test_validateVersion():
    assert validateVersion("v1") is True


def test_negative_validateVersion():
    assert validateVersion("1") is False


def test_validatePythonRule():
    assert validatePythonRule("hello.py") is True


def test_negative_validatePythonRule():
    with pytest.raises(
        Exception, match=f"python_rule does not match regex {pythonFilePathRegex}"
    ):
        validatePythonRule("hello.c")


def test_validateKafkaTopic():
    assert validateKafkaTopic("hello") is True


def test_negative_validateKafkaTopic():
    with pytest.raises(
        Exception, match=f"kafka_topic does not match regex {kafkaTopicRegex}"
    ):
        validateKafkaTopic("foor bar")
