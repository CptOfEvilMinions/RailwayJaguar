from confluent_kafka.admin import AdminClient
from pkg.config.load import Config
from typing import List


class KafaTopic(Exception):
    def __init__(self, ruleTopic: str):
        self.msg = f"Kafka does not have the following topic: {ruleTopic}"

    def __str__(self):
        return self.msg


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
            raise KafaTopic(rt)
