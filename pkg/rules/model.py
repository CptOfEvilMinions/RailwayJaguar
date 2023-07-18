from pkg.helpers.modules import LoadModule, GenerateModulePath
from typing import Dict, Any, List, Optional
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
    Name: str
    Description: str


@dataclass
class Test:
    __test__ = False
    Name: str
    Result: bool
    Event: Any


@dataclass
class RuleYaml(YAMLWizard):
    Version: str
    Kind: str
    PythonRule: str
    KafkaTopic: str
    Enabled: bool
    Metadata: Dict[str, Any]
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
        assert ruleYaml is not None
    return ruleYaml
