from pkg.helpers.modules import GenerateModulePath
from prometheus_client import start_http_server
from pkg.server.app import RegisterFaustApp
from pkg.server.agent import RegisterAgent
from pkg.config.load import ReadConfig
from pkg.ingest.kafka import (
    InitAdminClient,
    CheckTopics,
    ListTopics,
)
from pkg.rules.load import (
    GenerateListOfRules,
    LoadRuleModule,
    LoadRulesYaml,
)
from typing import Dict, List
from types import ModuleType
import faust


###############
#    App      #
###############
app = faust.App


if __name__ == "__main__":

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
    kc = InitAdminClient(conf=config)
    kafkaTopics = ListTopics(kc)
    CheckTopics(kafkaTopics, ruleTopics)

    rulesDict: Dict[str, List[ModuleType]] = dict()
    for ruleYamlFilePath, rule in rules.items():
        # rules/zeek/malicious_dns.yml -> rules.zeek.malicious_dns
        python_rule_file_path = GenerateModulePath(ruleYamlFilePath, rule)
        mod = LoadRuleModule(python_rule_file_path)

        if rule.KafkaTopic in rulesDict:
            rulesDict[rule.KafkaTopic].append(mod)
        else:
            x: List[ModuleType] = list()
            x.append(mod)
            rulesDict[rule.KafkaTopic] = x

    # Start up the server to expose the metrics.
    start_http_server(8000)

    # Start Faust Agents for each topic with
    # correlated rules
    for kafkaTopic, modules in rulesDict.items():
        RegisterAgent(app=app, topicName=kafkaTopic, rules=rulesDict[kafkaTopic])

    app.main()
