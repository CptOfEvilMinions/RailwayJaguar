from prometheus_client import start_http_server
from pkg.server.app import RegisterFaustApp
from pkg.outputs.loader import CheckOutputs
from pkg.outputs.loader import LoadPlugins
from pkg.server.agent import RegisterAgent
from pkg.config.load import ReadConfig
from pkg.ingest.kafka import (
    InitAdminClient,
    CheckTopics,
    ListTopics,
)
from typing import Dict, List
import logging
import faust

###############
#    App      #
###############
app = faust.App


if __name__ == "__main__":
    #### Logger ####
    logger = logging.getLogger("RailwayJaguar")

    #### Load config ####
    config = ReadConfig("conf/server.yaml")

    #### Load plugins ####
    plugins = LoadPlugins(logger)

    #### Register Faust app ####
    app = RegisterFaustApp(
        config.App.Name,
        config.Kafka.BoostrapServers,
    )

    #### Load rules ####
    from pkg.rules.load import LoadRules
    from pkg.rules.model import Rule

    rules: List[Rule] = LoadRules()
    ruleTopics: List[str] = [rule.Metadata.KafkaTopic for rule in rules]

    #### Check rule outputs with plugins ####
    kc = InitAdminClient(conf=config)
    kafkaTopics = ListTopics(kc)
    CheckTopics(kafkaTopics, ruleTopics)

    #### Load output plugins
    from pkg.outputs.loader import LoadPlugins

    outputPlugins = LoadPlugins(logger=logger)

    #### Check rule topics against kafka topics ####
    CheckOutputs(rules=rules, outputPlugins=plugins)

    rulesDict: Dict[str, List[Rule]] = dict()
    for rule in rules:
        if rule.Metadata.KafkaTopic in rulesDict:
            rulesDict[rule.Metadata.KafkaTopic].append(rule)
        else:
            rulesDict[rule.Metadata.KafkaTopic] = [rule]

    # Start up the server to expose the metrics.
    start_http_server(8000)

    # Start Faust Agents for each topic with
    # correlated rules
    for kafkaTopic, rules in rulesDict.items():
        RegisterAgent(
            app=app,
            topicName=kafkaTopic,
            rules=rules,
            outputPlugins=outputPlugins,
        )

    app.main()
