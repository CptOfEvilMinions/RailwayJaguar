from unittest.mock import patch, mock_open
from pkg.rules.load import (
    ReadRuleYaml,
    LoadRuleModule,
    GenerateListOfRules,
    LoadRulesYaml
)


def test_readRuleYaml():
    ruleYaml = ReadRuleYaml("tests/rules/test/powershell_empire.yml")
    assert ruleYaml["version"] == "v1"
    assert ruleYaml["kind"] == "stream_alert"
    assert ruleYaml["python_rule"] == "powershell_empire.py"
    assert ruleYaml["kafka_topic"] == "sysmon"
    assert ruleYaml["enabled"] is True
    assert ruleYaml["metadata"]["name"] == "malicious community_id"
    assert ruleYaml["metadata"]["MITRE_ATTACK"]["sub_technique_id"] == "T1059.001"
    assert ruleYaml["metadata"]["MITRE_DEFEND"]["sub_technique_id"] == "D3-PSA"
    assert ruleYaml["metadata"]["RequiedFields"] == ["process.command_line"]


def test_negativeReadRuleYaml():
    fake_file_path = 'file/path/mock'
    yamlNotBool = """
    version: v1
    kind: stream_alert
    python_rule: "powershell_empire.py"
    kafka_topic: "sysmon"
    enabled: "true"
    metadata:
      name: "malicious community_id"
    tests: []"""
    with patch('pkg.rules.load.open', new=mock_open(read_data=yamlNotBool)) as _file:
        ruleYaml = ReadRuleYaml(fake_file_path)
        _file.assert_called_once_with(fake_file_path, 'r')
        print("hello0")
        print("hello0")
        print("hello0")
        print (ruleYaml)
        print("hello0")
        print("hello0")
        print("hello0")

    assert True is False


def test_loadRuleModule():
    assert True is False


def test_negativeLoadRuleModule():
    assert True is False


def test_GenerateListOfRules():
    assert True is False

def test_NegativeGenerateListOfRules():
    assert True is False

def test_LoadRulesYaml():
    assert True is False

def test_NegativeLoadRulesYaml():
    assert True is False