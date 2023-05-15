from pkg.helpers.modules import GenerateModulePath
from pkg.config.load import VerifyConfig
from argparse import ArgumentParser
from pkg.rules.load import (
    GenerateListOfRules,
    LoadRuleModule,
    ReadRuleYaml,
    Rule,
)
from pkg.config.load import ReadConfig, Config

__CLI_VERSION = "0.1"


def ValidateAppConfig(appConfigFilePath: str):
    c: Config = ReadConfig(appConfigFilePath)
    VerifyConfig(c)


def ValidateGlobRules(ruleGlob: str = "rules/**/*.yml"):
    """
    Validate all the rules in a glob file path

    Params:
        ruleGlob (str): Glob path to rules
    """
    for ruleMetdataFilePath in GenerateListOfRules(ruleGlob):
        print(ruleMetdataFilePath)
        ValidateRule(ruleMetdataFilePath)


def ValidateRule(ruleYamlFilePath: str) -> bool:
    """
    Validate a rule

    Params:
        ruleFilePath (str): File path to a rule's metadata YAML file

    Return:
        (bool): Whether the rule is valid
    """
    rule: Rule = ReadRuleYaml(ruleYamlFilePath)
    module_path = GenerateModulePath(ruleYamlFilePath, rule)

    mod = LoadRuleModule(module_path)
    for test in rule.Tests:
        if mod.rule(event=test.Event) is not test.Result:
            print(f"[-] - {ruleYamlFilePath} failed {test.Name}")
            return False
    print(f"[+] - {ruleYamlFilePath} passed all the tests")
    return True


if __name__ == "__main__":
    parser = ArgumentParser("RailwayJaguar CLI")
    subparsers = parser.add_subparsers(
        dest="command", required=True, help="commands help"
    )

    #### version command ####
    versionParser = subparsers.add_parser("version", help="Print CLI version")

    ############################ Test command ############################
    testParser = subparsers.add_parser("test", help="test command")
    testSubparser = testParser.add_subparsers(
        dest="test_command", required=True, help="sub command help"
    )

    #### rule sub-command ####
    ruleParser = testSubparser.add_parser("rule", help="test rule sub-command")
    ruleParser.add_argument(
        "--rule-yaml", type=str, help="Specify a file path to a rule"
    )
    ruleParser.add_argument(
        "--rule-glob", type=str, help="Specify a file glob to rules"
    )

    #### config sub-command ####
    configParser = testSubparser.add_parser("config", help="test config sub-command")
    configParser.add_argument(
        "--rule-yaml", type=str, help="Specify a file path to a rule"
    )
    configParser.add_argument(
        "--rule-glob", type=str, help="Specify a file glob to rules"
    )
    args = parser.parse_args()

    if args.command == "verion":
        print(f"Versoin: {__CLI_VERSION}")
    if args.command == "test":
        if args.test_command == "rule":
            if args.rule_yaml is not None:
                ValidateRule(args.rule_yaml)
            if args.rule_glob is not None:
                ValidateGlobRules(args.rule_glob)
        if args.test_command == "config":
            if args.rule_yaml is not None:
                ValidateAppConfig(args.rule_yaml)
