from types import ModuleType
import importlib


def GenerateModulePath(ruleYamlFilePath: str, rulePythonRule: str) -> str:
    """
    This module uses the path to the ruleYAML and `PythonRule` defined
    by the YAML file to find the Python rule module.

    tests.rules.powershell_empire -> tests/rules/powershell_empire.yml

    Parameters:
        ruleYamlFilePath (str): File path to rule YAMl metadata
        rule (Rule): RailwayJaguar rule

    Return:
        (str): Return module path to Python rule
    """
    return (
        ".".join(ruleYamlFilePath.split("/")[:-1]) + "." + rulePythonRule
    ).removesuffix(".py")


def LoadModule(filePath: str) -> ModuleType:
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
