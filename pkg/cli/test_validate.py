from pkg.cli.validate import (
    ValidateAppConfig,
    ValidateGlobRules,
    ValidateRule,
)
import unittest


class TestCLIValidators(unittest.TestCase):
    def test_validateAppConfig(self):
        self.assertIsNone(ValidateAppConfig("tests/conf/server.yml"))

    def test_validateRule(self):
        self.assertTrue(
            ValidateRule(
                "tests/rules/powershell_empire.yml",
            )
        )

    def test_validateGlobRules(self):
        self.assertIsNone(ValidateGlobRules(ruleGlob="tests/rules/*.yml"))
