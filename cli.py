from cli.yaml_checker import CheckRuleYaml
from typing import List, Dict, Any
import importlib
import argparse
import yaml
import glob


def get_all_rules(glogPath: str = "rules/**/*.yml") -> List[str]:
    return glob.glob(glogPath)


def read_rule_yaml(filePath: str) -> Dict[str, Any]:
    with open(filePath, "r") as f:
        rule_yaml = yaml.safe_load(f)
    return rule_yaml


def generate_module_path(filePath: str) -> str:
    return ".".join(filePath.split("/")).removesuffix(".yml")


def load_rule(modulePath: str):
    return importlib.import_module(modulePath)


def test_all_rules():
    for rule in get_all_rules():
        rule_yaml = read_rule_yaml(rule)
        CheckRuleYaml(rule_yaml)
        module_path = generate_module_path(rule)

        mod = load_rule(modulePath=module_path)
        for test in rule_yaml["tests"]:
            assert mod.rule(event=test["event"]) is test["result"]
        print (f"[+] - {rule} passed all the tests")


def test_glob_rules(globPath: str):
    for rule in get_all_rules(globPath):
        rule_yaml = read_rule_yaml(rule)
        CheckRuleYaml(rule_yaml)
        module_path = generate_module_path(rule)

        mod = load_rule(modulePath=module_path)
        for test in rule_yaml["tests"]:
            assert mod.rule(event=test["event"]) is test["result"]
        print (f"[+] - {rule} passed all the tests")


def test_rule(ruleFilePath: str):
    rule_yaml = read_rule_yaml(ruleFilePath)
    CheckRuleYaml(rule_yaml)
    module_path = generate_module_path(ruleFilePath)

    mod = load_rule(modulePath=module_path)
    for test in rule_yaml["tests"]:
        assert mod.rule(event=test["event"]) is test["result"]
    print (f"[+] - {ruleFilePath} passed all the tests")


if __name__ == "__main__":
    parser = argparse.ArgumentParser("RailwayJaguar CLI")
    subparsers = parser.add_subparsers(dest="command", required=True, help="Sub-commands help")

    #### Test sub-command ####
    test_parser = subparsers.add_parser("test", help="test command")
    test_parser.add_argument("--rule-yaml", type=str, help="Specify a file path to a rule")
    test_parser.add_argument("--rule-glob", type=str, help="Specify a file glob to rules")
    args = parser.parse_args()
    
    if args.command == "test":
        if args.rule_yaml is not None:
            test_rule(args.rule_yaml)
        if args.rule_glob is not None:
            test_glob_rules(args.rule_glob)
        else:
            test_all_rules()

    
            