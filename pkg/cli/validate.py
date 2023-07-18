from pkg.config.load import ReadConfig, Config
from pkg.rules.load import GenerateListOfRules
from pkg.config.load import VerifyConfig
from pkg.rules.load import Rule


def ValidateAppConfig(appConfigFilePath: str) -> None:
    """
    Load a config for Railwayjaguar

    """
    c: Config = ReadConfig(appConfigFilePath)
    VerifyConfig(c)


def ValidateGlobRules(ruleGlob: str = "rules/**/*.yml") -> None:
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
    rule: Rule = Rule(ruleYamlFilePath)
    for test in rule.Metadata.Tests:
        if rule.run(event=test.Event) is not test.Result:
            print(f"[-] - {ruleYamlFilePath} failed {test.Name}")
            return False
    print(f"[+] - {ruleYamlFilePath} passed all the tests")
    return True
