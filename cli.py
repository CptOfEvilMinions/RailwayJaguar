from pkg.config.load import (
    VerifyConfig
)
from pkg.rules.load import (
    GenerateListOfRules,
    ReadRuleYaml,
    LoadRuleModule,
)
import argparse


def generate_module_path(filePath: str) -> str:
    return ".".join(filePath.split("/")).removesuffix(".yml")



def test_all_rules():
    for rule in GenerateListOfRules():
        rule_yaml = ReadRuleYaml(rule)
        VerifyConfig(rule_yaml)
        module_path = generate_module_path(rule)

        mod = LoadRuleModule(module_path)
        for test in rule_yaml["tests"]:
            assert mod.rule(event=test["event"]) is test["result"]
        print(f"[+] - {rule} passed all the tests")


def test_glob_rules(globPath: str):
    for rule in GenerateListOfRules(globPath):
        rule_yaml = ReadRuleYaml(rule)
        VerifyConfig(rule_yaml)
        module_path = generate_module_path(rule)

        mod = LoadRuleModule(module_path)
        for test in rule_yaml["tests"]:
            assert mod.rule(event=test["event"]) is test["result"]
        print(f"[+] - {rule} passed all the tests")


def test_rule(ruleFilePath: str):
    rule_yaml = ReadRuleYaml(ruleFilePath)
    VerifyConfig(rule_yaml)
    module_path = generate_module_path(ruleFilePath)

    mod = LoadRuleModule(module_path)
    for test in rule_yaml["tests"]:
        assert mod.rule(event=test["event"]) is test["result"]
    print(f"[+] - {ruleFilePath} passed all the tests")


if __name__ == "__main__":
    parser = argparse.ArgumentParser("RailwayJaguar CLI")
    subparsers = parser.add_subparsers(
        dest="command", required=True, help="Sub-commands help"
    )

    #### Test sub-command ####
    test_parser = subparsers.add_parser("test", help="test command")
    test_parser.add_argument(
        "--rule-yaml", type=str, help="Specify a file path to a rule"
    )
    test_parser.add_argument(
        "--rule-glob", type=str, help="Specify a file glob to rules"
    )
    args = parser.parse_args()

    if args.command == "test":
        if args.rule_yaml is not None:
            test_rule(args.rule_yaml)
        if args.rule_glob is not None:
            test_glob_rules(args.rule_glob)
        else:
            test_all_rules()
