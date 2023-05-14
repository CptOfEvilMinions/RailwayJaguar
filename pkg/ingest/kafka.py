from confluent_kafka.admin import AdminClient
from pkg.config.load import Config
from typing import List


def InitAdminClient(conf: Config) -> AdminClient:
    c = {"bootstrap.servers": ",".join(conf.Kafka.BoostrapServers)}
    return AdminClient(c)


def ListTopics(kc: AdminClient) -> List[str]:
    # https://stackabuse.com/how-to-list-all-kafka-topics/
    topics: List[str] = kc.list_topics().topics
    return topics


def CheckTopics(kafkaTopics: List[str], ruleTopics: List[str]):
    for rt in ruleTopics:
        if rt not in kafkaTopics:
            raise Exception(f"Kafka does not have the following topic: {rt}")
