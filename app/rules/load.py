from typing import Dict, List, Any
import importlib
import glob
import yaml

def LoadRules() -> List[Dict[str, Any]]:
    """
    This function will load the YAML for each rule and
    return a List of Dicts.
    """
    rules: List[Dict[str, Any]] = list() 
    for rule in glob.glob("rules/**/*.yml"):
        with open(rule, "r") as f:
            rule_yaml = yaml.safe_load(f)
            rules.append(rule_yaml)
    return rules


def GetRuleTopics(rulesYaml: List[Dict[str, Any]]) -> List[str]:
    topics: List[str] = list()
    for rule in rulesYaml:
        topics.append(rule["kafka_topic"])
    return topics


def GetRuleModules() -> List[str]:
    rule_modules: List[Any] = list()
    for python_rule in glob.glob("rules/**/*.py"):
        print (python_rule)        
        module_path = ".".join(python_rule.split("/")).removesuffix(".py")
        mod = importlib.import_module(module_path)
        rule_modules.append(mod)
    return rule_modules
