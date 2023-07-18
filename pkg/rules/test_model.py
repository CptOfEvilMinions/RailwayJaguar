from pkg.rules.model import ReadRuleYaml, RuleYaml
import unittest


class Test(unittest.TestCase):
    def test_ReadRuleYaml(self):
        ruleYaml: RuleYaml = ReadRuleYaml("tests/rules/powershell_empire.yml")
        self.assertEqual(ruleYaml.Enabled, True)
        self.assertEqual(ruleYaml.KafkaTopic, "sysmon")
        self.assertEqual(ruleYaml.Kind, "stream_alert")

        self.assertEqual(ruleYaml.Metadata["MITRE_ATTACK"]["technique_id"], "T1059")
        self.assertEqual(
            ruleYaml.Metadata["MITRE_DEFEND"]["sub_technique_id"], "D3-PSA"
        )
        self.assertEqual(ruleYaml.Metadata["RequiedFields"], ["process.command_line"])

        self.assertEqual(ruleYaml.Outputs, ["example"])
        self.assertEqual(ruleYaml.PythonRule, "powershell_empire.py")
        self.assertEqual(ruleYaml.Tests[0].Name, "True positive - powershell empire")
        self.assertEqual(ruleYaml.Tests[1].Name, "False positive")
