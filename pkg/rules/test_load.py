from unittest.mock import patch, mock_open
from pkg.rules.load import (
    ReadRuleYaml,
    LoadRuleModule,
    GenerateListOfRules,
    LoadRulesYaml,
)
from types import ModuleType
import unittest


class Test(unittest.TestCase):
    def test_readRuleYaml(self):
        ruleYaml = ReadRuleYaml("tests/rules/test/powershell_empire.yml")
        self.assertEqual(ruleYaml.Version, "v1")
        self.assertEqual(ruleYaml.Kind, "stream_alert")
        self.assertEqual(ruleYaml.PythonRule, "powershell_empire.py")
        self.assertEqual(ruleYaml.KafkaTopic, "sysmon")
        self.assertTrue(ruleYaml.Enabled)
        self.assertEqual(ruleYaml.Metadata["name"], "malicious community_id")
        self.assertEqual(
            ruleYaml.Metadata["MITRE_ATTACK"]["sub_technique_id"], "T1059.001"
        )
        self.assertEqual(
            ruleYaml.Metadata["MITRE_DEFEND"]["sub_technique_id"], "D3-PSA"
        )
        self.assertEqual(ruleYaml.Metadata["RequiedFields"], ["process.command_line"])

    def test_negativeReadRuleYaml(self):
        fake_file_path = "file/path/mock"
        yamlNotBool = """
        version: v1
        kind: stream_alert
        python_rule: "powershell_empire.py"
        kafka_topic: "sysmon"
        enabled: "true"
        metadata:
        name: "malicious community_id"
        tests: []"""
        with self.assertRaises(Exception), patch(
            "pkg.rules.load.open", new=mock_open(read_data=yamlNotBool)
        ) as _file:
            _ = ReadRuleYaml(fake_file_path)
            _file.assert_called_once_with(fake_file_path, "r")

    def test_loadRuleModule(self):
        mod = LoadRuleModule(filePath="tests.rules.test.powershell_empire")
        self.assertEqual(mod.__name__, "tests.rules.test.powershell_empire")
        self.assertIsInstance(mod, ModuleType)

    def test_negativeLoadRuleModule(self):
        with self.assertRaises(ModuleNotFoundError):
            _ = LoadRuleModule(filePath="tests/rules/test/powershell_empire.py")

    def test_GenerateListOfRules(self):
        self.assertEqual(
            GenerateListOfRules(fileGlob="tests/rules/test/*.yml"),
            ["tests/rules/test/powershell_empire.yml"],
        )

    def test_LoadRulesYaml(self):
        rules = LoadRulesYaml(["tests/rules/test/powershell_empire.yml"])
        for ruleName, rule in rules.items():
            self.assertEqual(ruleName, "tests/rules/test/powershell_empire.yml")
            self.assertEqual(rule.Version, "v1")
            self.assertEqual(rule.Kind, "stream_alert")
            self.assertEqual(rule.PythonRule, "powershell_empire.py")
            self.assertEqual(rule.KafkaTopic, "sysmon")
            self.assertTrue(rule.Enabled)
            self.assertEqual(rule.Metadata["name"], "malicious community_id")
            self.assertEqual(
                rule.Metadata["MITRE_ATTACK"]["sub_technique_id"], "T1059.001"
            )
            self.assertEqual(
                rule.Metadata["MITRE_DEFEND"]["sub_technique_id"], "D3-PSA"
            )
            self.assertEqual(rule.Metadata["RequiedFields"], ["process.command_line"])
