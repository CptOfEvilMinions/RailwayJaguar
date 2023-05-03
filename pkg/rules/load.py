from dataclasses import dataclass
from dataclass_wizard import YAMLWizard
from pkg.rules.yaml_checker import (
    validateKind,
    validateKafkaTopic,
    validatePythonRule,
    validateVersion
)
from typing import Dict, Any, List
from types import ModuleType
import importlib
import glob


@dataclass
class Metadata:
    Name: str
    Description: str


@dataclass
class Test:
    Name: str
    Result: bool
    Event: Any


@dataclass
class Rule(YAMLWizard):
    Version: str
    Kind: str
    PythonRule: str
    KafkaTopic: str
    Enabled: bool
    Metadata: Dict[str, Any]
    Tests: List[Test]

    def __post_init__(self):
        validateVersion(self.Version)
        validateKind(self.Kind)
        validatePythonRule(self.PythonRule)
        validateKafkaTopic(self.KafkaTopic)
        validateTests(self.Tests)


def ReadRuleYaml(filePath: str) -> Rule:
    """
    Return dict of the yaml file

    Parameters:
        filePath (str): File path to YAML file to read

    Return:
        (Dict[str, Any]): Yaml in the form of a dictonary
        (yaml.YAMLError): YAML error when reading the file
    """
    with open(filePath, "r") as f:
        ruleYaml: Rule = ReadRuleYaml.from_yaml(f.read())
    return ruleYaml


def LoadRuleModule(filePath: str) -> ModuleType:
    """
    Load rule module 

    Parameters:
        filePath (str): File path rule module

    Return:
        (ModuleType): Rule module
        (Exception): Eerror when loading module
    """
    try:
        mod = importlib.import_module(filePath)
    except Exception as exc:
        raise exc
    return mod

def GenerateListOfRules(fileGlob: str = "rules/**/*.yml") -> List[str]:
    """
    Generate a list of YAML rule files for the specified glob

    Parameters:
        fileGlob (str): File Glob path to rules

    Return:
        (List[str]): List of file paths to YAML rule files
    """
    return glob.glob(fileGlob)


def LoadRulesYaml(ruleYamlsFilePaths: List[str]) -> Dict[str, Rule]:
    """
    Generate a dict of rules for the for the specified 
    list of YAML rule files

    Parameters:
        ruleYamlsFilePaths (List[str]): List of file paths to YAML rule files

    Return:
        (Dict[str, Rule]): Dict of rule file paths to rules obj
    """
    rules: Dict[str, Rule] = dict()
    for ruleYamlFilePath in ruleYamlsFilePaths:
        rule = ReadRuleYaml(ruleYamlFilePath)
        if rule.Enabled is True:
            rules[ruleYamlFilePath] = rule
    return rules



