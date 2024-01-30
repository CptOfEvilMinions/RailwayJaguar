from pkg.helpers.modules import LoadModule, GenerateModulePath
from typing import Dict, Any, List, Optional, TypedDict
from dataclass_wizard import YAMLWizard
from pkg.rules.validate import (
    validateKind,
    validateKafkaTopic,
    validatePythonRule,
    validateVersion,
)
from dataclasses import dataclass
from types import ModuleType


class Rule:
    """
    A class to represent Rule

    Attributes:
        yamlRulePath: str
            File path to rule YAML
    """

    def __init__(self, yamlRulePath: str) -> None:
        self.__yamlRulePath: str = yamlRulePath
        self.Metadata: RuleYaml = ReadRuleYaml(self.__yamlRulePath)
        self.PythonRule: ModuleType = LoadModule(
            GenerateModulePath(yamlRulePath, self.Metadata.PythonRule)
        )

    def run(self, event: Any) -> bool:
        return self.PythonRule.rule(event=event)


@dataclass
class Metadata:
    """
    Rule YAML dataclass for ingesting rule metadata from YAML

    Args:
        Name (str): Name of test
        Description (str):
    """

    Name: str
    Description: str


@dataclass
class Test:
    """
    Rule YAML dataclass for ingesting rule metadata from YAML

    Args:
        Name (str): Name of test
        Result (bool): Expected result for test
        Event (TypedDict): Test event, typically in JSON format
    """

    __test__ = False
    Name: str
    Result: bool
    Event: TypedDict


@dataclass
class RuleYaml(YAMLWizard):
    """
    Rule YAML dataclass for ingesting rule metadata from YAML

    Args:
        Version (str): Rule YAML config version
        Kind (str): Specify rule type
        PythonRule (str): Specify file name of Python rule
        KafkaTopic (str): Specify kafka topic to ingest events from for rule
        Enabled (bool): Whether rule is enabled/disabled
        Metadata (Dict[str, TypedDict]): Rule metadata
        Outputs (List[str]): List of output plugins to send alert too
        Tests (Optional[List[Test]]): List of test events for rule
    """

    Version: str
    Kind: str
    PythonRule: str
    KafkaTopic: str
    Enabled: bool
    Metadata: Dict[str, TypedDict]
    Outputs: List[str]
    Tests: Optional[List[Test]]

    def __post_init__(self):
        validateVersion(self.Version)
        validateKind(self.Kind)
        validatePythonRule(self.PythonRule)
        validateKafkaTopic(self.KafkaTopic)


def ReadRuleYaml(filePath: str) -> RuleYaml:
    """
    Read the rule metadata YAML file

    Parameters:
        filePath (str): File path to YAML file to read

    Return:
        ruleYaml (Rule): Return rule metadata

    """
    with open(filePath, "r") as f:
        ruleYaml: RuleYaml = RuleYaml.from_yaml(f.read())
    return ruleYaml
