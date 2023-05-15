from pkg.helpers.modules import GenerateModulePath
from pkg.rules.load import ReadRuleYaml
from pkg.rules.load import Rule
import unittest


class Test(unittest.TestCase):
    """
    # rules/zeek/malicious_dns.yml -> rules.zeek.malicious_dns
    """

    def test_generateModulePath(self):
        ruleYamlFilePath: str = "tests/rules/test/powershell_empire.yml"
        rule: Rule = ReadRuleYaml(ruleYamlFilePath)

        self.assertEqual(
            GenerateModulePath(ruleYamlFilePath, rule),
            "tests.rules.test.powershell_empire",
        )
