from dataclasses import dataclass
from dataclass_wizard import YAMLWizard
from urllib.parse import urlparse
from typing import List
import re 

@dataclass
class App:
    name: str

@dataclass
class Kafka:
    boostrap_servers: List[str]

@dataclass
class Secret:
    vault_addr: str
    vault_token: str

@dataclass
class Config(YAMLWizard):
    kafka: Kafka
    app: App
    secret: Secret


def validateName(app: str) -> bool:
    # https://regex101.com/r/UgwsEO/1
    appRegex = r"^\w+$"
    if bool(re.match(appRegex, app)):
        return True
    else:
        raise Exception("app name does not match regex r\"^\\w+$\"")


def validateKafka(kafka: Kafka) -> bool:
    if isinstance(kafka.boostrap_servers, list) is False:
        raise Exception("""Kafka boostrap_servers need to be defined as a list. 
        Example:

        kafka:
          boostrap_servers: 
            - kafka.hackinglab.local:9092
        """)
    for bserver in kafka.boostrap_servers:
        if bool(urlparse(bserver)) is False:
            raise Exception("Invalid bootstrap server: {bserver}")
    return True


def validateSecret(secret: Secret) -> bool:
    # https://discuss.hashicorp.com/t/what-is-regex-pattern-for-hashicorp-vault-tokens/50502/2
    vaultRegex = r"hv[sb]\.(?:[A-Za-z0-9]{24}|[A-Za-z0-9_-]{91,})"
    if bool(urlparse(secret.vault_addr)) is False:
        raise Exception("Invalid vault address: {bserver}")
    if bool(re.match(vaultRegex, secret.vault_token)) is False:
        raise Exception("Invalid vault token")
    return True


def ReadConfig(filePath: str) -> Config:
    """
    Reads a YAML config for server

    Parameters:
        filePath (str): File path to config

    Return:
        (Config): Config data model for YAML config
    """
    with open(filePath, "r") as f:
        c: Config = Config.from_yaml(f.read())
        VerifyConfig(c)
    return c

def VerifyConfig(c: Config) -> bool:
    validateName(c.app.name)
    validateKafka(c.Kafka)
    validateSecret(c.Secret)
    return True

