from cli import (
    ValidateAppConfig,
    ValidateGlobRules,
    ValidateRule,
)
import unittest


class Test(unittest.TestCase):
    def test_validateAppConfig(self):
        self.assertIsNone(ValidateAppConfig("tests/conf/server.yml"))

    def test_validateGlobRules(self):
        self.assertIsNone(ValidateGlobRules("tests/rules/test/*.yml"))

    def test_validateRule(self):
        self.assertTrue(ValidateRule("tests/rules/test/powershell_empire.yml"))
