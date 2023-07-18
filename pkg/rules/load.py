from pkg.rules.model import RuleYaml, ReadRuleYaml, Rule
from typing import Dict, List
import glob


def GenerateListOfRules(fileGlob: str = "rules/**/*.yml") -> List[str]:
    """
    Generate a list of YAML rule files for the specified glob

    Parameters:
        fileGlob (str): File Glob path to rules

    Return:
        (List[str]): List of file paths to YAML rule files
    """
    return glob.glob(fileGlob)


def LoadRulesYaml(ruleYamlsFilePaths: List[str]) -> Dict[str, RuleYaml]:
    """
    Generate a dict of rules for the for the specified
    list of YAML rule files

    Parameters:
        ruleYamlsFilePaths (List[str]): List of file paths to YAML rule files

    Return:
        (Dict[str, Rule]): Dict of rule file paths to rules obj
    """
    rulesYaml: Dict[str, RuleYaml] = dict()
    for ruleYamlFilePath in ruleYamlsFilePaths:
        rule = ReadRuleYaml(ruleYamlFilePath)
        if rule.Enabled is True:
            rulesYaml[ruleYamlFilePath] = rule
    return rulesYaml


def LoadRules() -> List[Rule]:
    """
    Load rules

    Return:
        A list of rules
    """
    rules: List[Rule] = []
    for ruleYamlPath in GenerateListOfRules():
        rule = Rule(ruleYamlPath)
        if rule.Metadata.Enabled:
            rules.append(rule)
    return rules
