from prometheus_client import start_http_server
from pkg.server.worker import RegisterWorker
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
    #subparsers = parser.add_subparsers(dest="command", required=True, help="Sub-commands help")
    ##parser.add_argument("--config", required=True, type=str, help="Specify a file path to a rule")

    #### Test sub-command ####
    #test_parser = subparsers.add_parser("test", help="test command")
    #test_parser.add_argument("--rule-yaml", type=str, help="Specify a file path to a rule")
    #test_parser.add_argument("--rule-glob", type=str, help="Specify a file glob to rules")
    ##args = parser.parse_args()

    ##### Load config ####
    ##config = ReadConfig(args.config)
    config = ReadConfig("conf/server.yaml")

    #### Register Faust app ####
    app = RegisterFaustApp(
        config.app.name,
        config.kafka.boostrap_servers,
    )

    #### Load rules ####
    rules = LoadRulesYaml(GenerateListOfRules())
    ruleTopics = [v["kafka_topic"] for _,v in rules.items()]
    
    #### Check rule topics against kafka topics ####
    ##kc = InitAdminClient(conf=config)
    ##kafkaTopics = ListTopics(kc)
    ##CheckTopics(kafkaTopics, ruleTopics)

    rules_dict: Dict[str, List[ModuleType]] = dict()
    for ruleYamlFilePath, yaml_rule in rules.items():
        # rules/zeek/malicious_dns.yml -> rules.zeek.malicious_dns
        python_rule_file_path: str = (
            "/".join(ruleYamlFilePath.split("/")[:2])
            + "/"
            + yaml_rule["python_rule"]
        ).removesuffix(".py").replace("/", ".")

        mod = LoadRuleModule(python_rule_file_path)

        if yaml_rule["kafka_topic"] in rules_dict:
            rules_dict[yaml_rule["kafka_topic"]].append(mod)
        else:
            x: List[ModuleType] = list()
            x.append(mod)
            rules_dict[yaml_rule["kafka_topic"]] = x

    # Start up the server to expose the metrics.
    start_http_server(8000)

    
    for kafka_topic, modules in rules_dict.items():
        t = app.topic(kafka_topic, value_type=str)
        for rule in rules_dict[kafka_topic]:
            print(f"[*] - Registering {rule.__name__} on kafka topic: {kafka_topic}")
        rules = rules_dict[kafka_topic]
        RegisterWorker(app, t, rules=rules)

    
    # t = app.topic("zeek_conn", value_type=str)
    # for rule in rules_dict["zeek_conn"]:
    #     print(f"[*] - Registering {rule.__name__} on kafka topic: zeek_conn")
    # rules = rules_dict["zeek_conn"]
    # RegisterWorker(app, t, rules=rules)

    # t = app.topic("zeek_dns", value_type=str)
    # for rule in rules_dict["zeek_dns"]:
    #     print(f"[*] - Registering {rule.__name__} on kafka topic: zeek_dns")
    # rules = rules_dict["zeek_dns"]
    # RegisterWorker(app, t, rules=rules)

    app.main()

    #     print (rule)

    # import glob
    # import yaml
    # import importlib

    # blah = dict()
    # for yaml_rule_file_path in glob.glob("rules/**/*.yml"):
    #     with open(yaml_rule_file_path, "r") as f:
    #         yaml_rule = yaml.safe_load(f)
    #     python_rule_file_path = (
    #         "/".join(yaml_rule_file_path.split("/")[:2])
    #         + "/"
    #         + yaml_rule["python_rule"]
    #     )

    #     mod = importlib.import_module(
    #         python_rule_file_path.removesuffix(".py").replace("/", ".")
    #     )
    #     if yaml_rule["kafka_topic"] in blah:
    #         blah[yaml_rule["kafka_topic"]].append(mod)
    #     else:
    #         x = list()
    #         x.append(mod)
    #         blah[yaml_rule["kafka_topic"]] = x

    

    # for kafka_topic, modules in blah.items():
    #     t = app.topic(kafka_topic, value_type=str)
    #     for rule in blah[kafka_topic]:
    #         print(f"[*] - Registering {rule.__name__} on kafka topic: {kafka_topic}")
    #     rules = blah[kafka_topic]
    #     RegisterWorker(app, t, rules=rules)



    
