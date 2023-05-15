from pkg.rules.load import Rule


def GenerateModulePath(ruleYamlFilePath: str, rule: Rule) -> str:
    """
    This module uses the path to the ruleYAML and `PythonRule` defined
    by the YAML file to find the Python rule module.

    tests.rules.test.powershell_empire -> tests/rules/test/powershell_empire.yml

    Parameters:
        ruleYamlFilePath (str): File path to rule YAMl metadata
        rule (Rule): RailwayJaguar rule

    Return:
        (str): Return module path to Python rule
    """
    return (
        ".".join(ruleYamlFilePath.split("/")[:-1]) + "." + rule.PythonRule
    ).removesuffix(".py")
