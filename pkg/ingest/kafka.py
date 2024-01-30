from confluent_kafka.admin import AdminClient
from pkg.config.load import Config
from typing import List


class KafaTopic(Exception):
    def __init__(self, ruleTopic: str):
        self.msg = f"Kafka does not have the following topic: {ruleTopic}"

    def __str__(self):
        return self.msg


def InitAdminClient(conf: Config) -> AdminClient:
    """
    Create a Kafka client

    Params:
        conf (Config) - Config instance contains how to connect to Kafka

    Returns:
        c: Return Kafka client
    """
    c = {"bootstrap.servers": ",".join(conf.Kafka.BoostrapServers)}
    return AdminClient(c)


def ListTopics(kc: AdminClient) -> List[str]:
    """
    Return a list of Kafka topics

    Params:
        kc (AdminClient) - Kafka client

    Returns:
        c: Return list of Kafka topics
    """
    # https://stackabuse.com/how-to-list-all-kafka-topics/
    topics: List[str] = kc.list_topics().topics
    return topics


def CheckTopics(kafkaTopics: List[str], ruleTopics: List[str]):
    """
    Check that topics specified in rules exist

    Params:
        kafkaTopics (List[str]) - List of Kafka topics
        ruleTopics (List[str]) - List of topics used by rules

    Raises:
        KafaTopic: Topic doesn't exist
    """
    for rt in ruleTopics:
        if rt not in kafkaTopics:
            raise KafaTopic(rt)
