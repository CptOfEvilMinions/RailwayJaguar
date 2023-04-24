from app.rules.load import (
    LoadRules, 
    GetRuleTopics,
    GetRuleModules,
)
from typing import Any, Dict, List
import argparse
import faust


__FAUST_APP = faust.App("zeek", broker="kafka://kafka.hackinglab.local:9092")


def register_worker(t, rules: List[Any]):
    """
    Register a faust worker for each 
    Kafka topic.
    """
    @__FAUST_APP.agent(t)
    async def match(events: List[Dict[str, Any]]):
        async for event in events:
            for blah in rules:
                if blah.rule(event=event):
                    print (event)

if __name__ == "__main__":
    # rules = LoadRules()
    # for kt in GetRuleTopics(rules):
    #     t = __FAUST_APP.topic(kt,value_type=str)
    #     __FAUST_TOPICS.append(t)

    # rule_modules = GetRuleModules()
    # print(rule_modules)

    import glob
    import yaml
    import importlib
    blah = dict()
    for yaml_rule_file_path in glob.glob("rules/**/*.yml"):
        with open(yaml_rule_file_path, "r") as f:
            yaml_rule = yaml.safe_load(f)
        python_rule_file_path =  (
            '/'.join(yaml_rule_file_path.split("/")[:2]) + 
            "/" + 
            yaml_rule["python_rule"]
        )


        mod = importlib.import_module(python_rule_file_path.removesuffix(".py").replace("/", ".") )
        if yaml_rule["kafka_topic"] in blah:
            blah[yaml_rule["kafka_topic"]].append(mod)
        else:
            x = list()
            x.append(mod)
            blah[yaml_rule["kafka_topic"]] = x


    for kafka_topic, modules in blah.items():
        t = __FAUST_APP.topic(kafka_topic,value_type=str)
        for rule in blah[kafka_topic]:
            print (f"[*] - Registering {rule.__name__} on kafka topic: {kafka_topic}")
        rules = blah[kafka_topic]
        register_worker(t, rules=rules)

        

    # for ft in __FAUST_TOPICS:
    #     rule_modules
    #     for topic

    # for ft in __FAUST_TOPICS:
    #     @app.agent(ft)
    #     async def match(events: List[Dict[str, Any]]):
    #         async for event in events:
    #             if rule(event=event):
    #                 print (event)

    # parser = argparse.ArgumentParser("RailwayJaguar server")
    # subparsers = parser.add_subparsers(dest="command", required=True, help="Sub-commands help")

    # #### Test sub-command ####
    # test_parser = subparsers.add_parser("test", help="test command")
    # test_parser.add_argument("--rule-yaml", type=str, help="Specify a file path to a rule")
    # test_parser.add_argument("--rule-glob", type=str, help="Specify a file glob to rules")
    # args = parser.parse_args()

    print (__FAUST_APP)
    __FAUST_APP.main()


    # parser = argparse.ArgumentParser()
    # test(parser=parser)
    # args = parser.parse_args()
    # print (args)

    # if args.rules_dir_glob:
    #     TestRules(args.rules_dir_glob)
    # elif args.metadata:
    #     TestRule(args.metadata)
    # else:
    #     print ("Command is not supported")
    #     sys.exit(1)