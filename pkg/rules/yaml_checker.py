from typing import Dict, Any
import re

# https://regex101.com/r/Qkq6yi/1
kafkaTopicRegex = r"^[a-zA-Z0-9-_]+$"

# https://regex101.com/r/Qkq6yi/1
pythonFilePathRegex = r"[a-zA-Z0-9-_]+.py"

def validateKind(kind: str) -> bool:
    if kind == "stream_alert":
        return True
    else:
        raise Exception("kind is not a known type: [stream_alert]")


def validateVersion(version: str) -> bool:
    if version == "v1":
        return True
    else:
        raise Exception(f"Invalid version string please use v1")


def validatePythonRule(pythonFilePath: str) -> bool:
    if bool(re.match(pythonFilePathRegex, pythonFilePath)):
        return True
    else:
        raise Exception(f"python_rule does not match regex {pythonFilePathRegex}")


def validateKafkaTopic(kafkaTopic: str) -> bool:
    if bool(re.match(kafkaTopicRegex, kafkaTopic)):
        return True
    else:
        raise Exception(f"kafka_topic does not match regex {kafkaTopicRegex}")


def CheckRuleYaml(yamlDict: Dict[str, Any]) -> bool:
    if (
        validateVersion(yamlDict["version"])
        and validateKind(yamlDict["kind"])
        and validatePythonRule(yamlDict["python_rule"])
        and validateKafkaTopic(yamlDict["kafka_topic"])
    ):
        return True
    return False
