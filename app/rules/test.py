import textwrap
import yaml
import glob


def successMessage(ruleName: str, testName: str):
    print (textwrap.dedent(f"""
        ---
        Rule name: {ruleName}
        Test name: {testName}"""))
    
def failureMessage(ruleName: str, testName: str):
    print (textwrap.dedent(f"""
        ---
        Rule name: {ruleName}
        Test name: {testName}"""))
    

def TestRule(metaDataFile: str):
    """Test detection rule logic"""
    with open(metaDataFile, "r") as f:
        ruleMetaData = yaml.safe_load(f)
        command_module = __import__(
            # rules.zeek.malicious_ip_addr
            metaDataFile.strip(".yml").replace("/","."),
            # rules.zeek
            fromlist=[".".join(metaDataFile.replace("/", ".").split(".")[:-1])]
        )
        for test in ruleMetaData["tests"]:
            if test["result"] == command_module.rule(test["event"]):
                successMessage(ruleMetaData["rule_name"],test["name"])
            else:
                failureMessage(ruleMetaData["rule_name"],test["name"])
                

def TestRules(rulesGlob: str):
    """Test detection rule logic in glob path"""
    for rule in glob.glob(rulesGlob):
        with open(rule, "r") as f:
            ruleMetaData = yaml.safe_load(f)
            command_module = __import__(
                # rules.zeek.malicious_ip_addr
                rule.strip(".yml").replace("/","."),
                # rules.zeek
                fromlist=[".".join(rule.replace("/", ".").split(".")[:-1])]
            )
            for test in ruleMetaData["tests"]:
                if test["result"] == command_module.rule(test["event"]):
                    successMessage(ruleMetaData["rule_name"],test["name"])
                else:
                    failureMessage(ruleMetaData["rule_name"],test["name"])
