from typing import Dict, TypedDict
import re

# https://regex101.com/r/Qkq6yi/1
kafkaTopicRegex = r"^[a-zA-Z0-9-_]+$"

# https://regex101.com/r/Qkq6yi/1
pythonFilePathRegex = r"[a-zA-Z0-9-_]+.py"


class RuleConfigError(Exception):
    pass


class InvalidKind(RuleConfigError):
    def __init__(self):
        self.msg = "kind is not a known type: [stream_alert]"

    def __str__(self):
        return self.msg


class InvalidVersion(RuleConfigError):
    def __init__(self):
        self.msg = "Invalid version string please use v1"

    def __str__(self):
        return self.msg


class InvalidPythonRule(RuleConfigError):
    def __init__(self):
        self.msg = f"python_rule does not match regex {pythonFilePathRegex}"

    def __str__(self):
        return self.msg


class InvalidKafkaTopic(RuleConfigError):
    def __init__(self):
        self.msg = f"kafka_topic does not match regex {kafkaTopicRegex}"

    def __str__(self):
        return self.msg


def validateKind(kind: str) -> bool:
    if kind == "stream_alert":
        return True
    else:
        raise InvalidKind


def validateVersion(version: str) -> bool:
    if version == "v1":
        return True
    else:
        raise InvalidVersion


def validatePythonRule(pythonFilePath: str) -> bool:
    if bool(re.match(pythonFilePathRegex, pythonFilePath)):
        return True
    else:
        raise InvalidPythonRule


def validateKafkaTopic(kafkaTopic: str) -> bool:
    if bool(re.match(kafkaTopicRegex, kafkaTopic)):
        return True
    else:
        raise InvalidKafkaTopic


def CheckRuleYaml(yamlDict: Dict[str, TypedDict]) -> bool:
    if (
        validateVersion(yamlDict["version"])
        and validateKind(yamlDict["kind"])
        and validatePythonRule(yamlDict["python_rule"])
        and validateKafkaTopic(yamlDict["kafka_topic"])
    ):
        return True
    return False
