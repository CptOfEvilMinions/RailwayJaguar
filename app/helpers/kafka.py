from confluent_kafka import Consumer
from typing import List

def ListTopics(kc: Consumer) -> List[str]:
    return kc.list_topics()