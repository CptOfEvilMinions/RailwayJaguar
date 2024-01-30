from pkg.helpers.modules import GenerateModulePath, LoadModule
from pkg.rules.load import ReadRuleYaml
from pkg.rules.load import RuleYaml
from types import ModuleType
import unittest


class TestModuleHelpers(unittest.TestCase):
    """
    Convert file path of rule YAML to python pkg dir format

    rules/zeek/malicious_dns.yml -> rules.zeek.malicious_dns
    """

    def test_GenerateModulePath(self):
        ruleYamlFilePath: str = "tests/rules/powershell_empire.yml"
        ruleYaml: RuleYaml = ReadRuleYaml(ruleYamlFilePath)

        self.assertEqual(
            GenerateModulePath(ruleYamlFilePath, ruleYaml.PythonRule),
            "tests.rules.powershell_empire",
        )

    def test_LoadModule(self):
        # Load rule YAML
        ruleYamlFilePath: str = "tests/rules/powershell_empire.yml"
        ruleYaml: RuleYaml = ReadRuleYaml(ruleYamlFilePath)

        # Load rule as Python module
        mod: ModuleType = LoadModule(
            GenerateModulePath(ruleYamlFilePath, ruleYaml.PythonRule)
        )
        self.assertIsInstance(mod, ModuleType)

        self.assertEqual("tests.rules.powershell_empire", mod.__name__)
