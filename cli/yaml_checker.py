from typing import Dict, Any, Set, List
import re

REQUIRED_KEYS: Set[str] = {
    "version",
    "kind",
    "python_rule", 
    "kafka_topic", 
    "tests",
}


def check_required_fields(yamlKeys: Set[str]) -> bool:
    if REQUIRED_KEYS == yamlKeys:
        return True
    else:
        raise Exception("YAML does not include all the required keys")


def check_kind(kind: str) -> bool:
    if kind == "stream_alert":
        return True
    else:
        raise Exception("kind is not a known type: [stream_alert]")


def check_version(version: str) -> bool:
    if version == "v1":
        return True
    else:
        raise Exception("version is not a known version")


def check_python_rule(pythonFilePath: str) -> bool:
    # https://regex101.com/r/Qkq6yi/1
    pythonFilePathRegex = r"[a-zA-Z0-9-_]+.py"
    if bool(re.match(pythonFilePathRegex, pythonFilePath)):
        return True
    else:
        raise Exception("python_rule does not match regex {pythonFilePathRegex}")


def check_kafka_topic(kafkaTopic: str) -> bool:
    # https://regex101.com/r/Qkq6yi/1
    kafkaTopicRegex = r"[a-zA-Z0-9-_]"
    if bool(re.match(kafkaTopicRegex, kafkaTopic)):
        return True
    else:
        raise Exception("kafka_topic does not match regex {kafkaTopicRegex}")


def check_tests(tests: List[Dict[str, Any]]) -> bool:
    for test in tests:
        if "name" not in test:
            raise Exception("test name does not exist")
        if not isinstance(test["result"], bool):
            raise Exception("test result is not a boolean value")
        if not (
            isinstance(test["event"], Dict) or
            isinstance(test["event"], str)
        ):
            raise Exception("test event is not a dict(JSON) or a string")
    return True
            

def CheckRuleYaml(yamlDict: Dict[str, Any]):
    if (
        check_version(yamlDict["version"]) and
        check_kind(yamlDict["kind"]) and
        check_required_fields(set(yamlDict.keys())) and
        check_python_rule(yamlDict["python_rule"]) and
        check_kafka_topic(yamlDict["kafka_topic"]) and
        check_tests(yamlDict["tests"])
    ):
        return True
    
