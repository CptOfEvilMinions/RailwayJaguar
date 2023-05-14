from prometheus_client import start_http_server
from pkg.server.agent import RegisterAgent
from pkg.server.app import RegisterFaustApp
from pkg.config.load import ReadConfig
from typing import Dict, List
from types import ModuleType
from pkg.ingest.kafka import (
    InitAdminClient,
    CheckTopics,
    ListTopics,
)
from pkg.rules.load import (
    LoadRulesYaml,
    GenerateListOfRules,
    LoadRuleModule,
)
import argparse
import faust


###############
#    App      #
###############
app = faust.App

if __name__ == "__main__":
    ##parser = argparse.ArgumentParser("RailwayJaguar server")
    # subparsers = parser.add_subparsers(dest="command", required=True, help="Sub-commands help")
    ##parser.add_argument("--config", required=True, type=str, help="Specify a file path to a rule")

    #### Test sub-command ####
    # test_parser = subparsers.add_parser("test", help="test command")
    # test_parser.add_argument("--rule-yaml", type=str, help="Specify a file path to a rule")
    # test_parser.add_argument("--rule-glob", type=str, help="Specify a file glob to rules")
    ##args = parser.parse_args()

    ##### Load config ####
    ##config = ReadConfig(args.config)
    config = ReadConfig("conf/server.yaml")

    #### Register Faust app ####
    app = RegisterFaustApp(
        config.App.Name,
        config.Kafka.BoostrapServers,
    )

    #### Load rules ####
    rules = LoadRulesYaml(GenerateListOfRules())
    ruleTopics = [v.KafkaTopic for _, v in rules.items()]

    #### Check rule topics against kafka topics ####
    ##kc = InitAdminClient(conf=config)
    ##kafkaTopics = ListTopics(kc)
    ##CheckTopics(kafkaTopics, ruleTopics)

    rulesDict: Dict[str, List[ModuleType]] = dict()
    for ruleYamlFilePath, yamlRule in rules.items():
        # rules/zeek/malicious_dns.yml -> rules.zeek.malicious_dns
        python_rule_file_path: str = (
            ("/".join(ruleYamlFilePath.split("/")[:2]) + "/" + yamlRule.PythonRule)
            .removesuffix(".py")
            .replace("/", ".")
        )

        mod = LoadRuleModule(python_rule_file_path)

        if yamlRule.KafkaTopic in rulesDict:
            rulesDict[yamlRule.KafkaTopic].append(mod)
        else:
            x: List[ModuleType] = list()
            x.append(mod)
            rulesDict[yamlRule.KafkaTopic] = x

    # Start up the server to expose the metrics.
    start_http_server(8000)

    # Start Faust Agents for each topic with
    # correlated rules
    for kafkaTopic, modules in rulesDict.items():
        RegisterAgent(app=app, topicName=kafkaTopic, rules=rulesDict[kafkaTopic])

    app.main()
