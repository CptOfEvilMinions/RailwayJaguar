from dataclasses import dataclass
from dataclass_wizard import YAMLWizard
from typing import List
import sys

@dataclass
class Config(YAMLWizard):
    KafkaBootstrapServers: List[str]
    kafkaTopic: str


def ReadConfig(filePath: str) -> Config:
    c = Config()
    with open(filePath, "r") as f:
        c: Config = Config.from_yaml(f)
        if not VerifyConfig(c):
            sys.exit(1)
    return c
    

def verifyKafkaBootstrapServers(kafkaBootstrapServers: List[str]) -> bool:
    for ks in kafkaBootstrapServers:
        bs = ks.split(":")
        if bs[0] is not str:
            return False
        if bs[1] is not int:
            return False
    return True

def VerifyConfig(c: Config) -> bool:
    if not verifyKafkaBootstrapServers(c.KafkaBootstrapServers):
        return False
    return True