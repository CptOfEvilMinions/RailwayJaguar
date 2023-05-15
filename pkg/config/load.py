from dataclasses import dataclass
from dataclass_wizard import YAMLWizard
from urllib.parse import urlparse
from typing import List, Optional
import re


class AppConfigError(Exception):
    pass


class InvalidName(AppConfigError):
    def __init__(self):
        self.msg = 'app name does not match regex r"^\\w+$"'

    def __str__(self):
        return self.msg


class InvalidBootstrapServer(AppConfigError):
    """Invalid bootstrap server"""

    def __init__(self, bserver: str):
        self.msg = f"Invalid bootstrap server: {bserver}"

    def __str__(self):
        return self.msg


class InvalidVaultAddr(AppConfigError):
    """Invalid Vault Address"""

    def __init__(self, addr: str):
        self.msg = f"Invalid vault address: {addr}"

    def __str__(self):
        return self.msg


class InvalidVaultSecret(AppConfigError):
    """Invalid Vault Secret name"""

    def __init__(self):
        self.msg = "Invalid vault token"

    def __str__(self):
        return self.msg


@dataclass
class App:
    Name: str


@dataclass
class Kafka:
    BoostrapServers: List[str]


@dataclass
class Secret:
    VaultAddr: str
    VaultToken: str


@dataclass
class Config(YAMLWizard):
    Kafka: Kafka
    App: App
    Secret: Optional[Secret]


def validateName(app: str) -> bool:
    # https://regex101.com/r/UgwsEO/1
    appRegex = r"^\w+$"
    if bool(re.match(appRegex, app)):
        return True
    else:
        raise InvalidName


def validateKafka(kafka: Kafka) -> bool:
    for bserver in kafka.BoostrapServers:
        if bool(urlparse(bserver)) is False:
            raise InvalidBootstrapServer(bserver=bserver)
    return True


def validateSecret(secret: Secret) -> bool:
    # https://discuss.hashicorp.com/t/what-is-regex-pattern-for-hashicorp-vault-tokens/50502/2
    vaultRegex = r"hv[sb]\.(?:[A-Za-z0-9]{24}|[A-Za-z0-9_-]{91,})"
    if bool(urlparse(secret.VaultAddr)) is False:
        raise InvalidVaultAddr(addr=secret.VaultAddr)
    if bool(re.match(vaultRegex, secret.VaultToken)) is False:
        raise InvalidVaultSecret()
    return True


def ReadConfig(filePath: str) -> Config:
    """
    Reads a YAML config for server

    Params:
        filePath (str): File path to config

    Return:
        (Config): Config data model for YAML config
    """
    with open(filePath, "r") as f:
        c: Config = Config.from_yaml(f.read())
        VerifyConfig(c)
    return c


def VerifyConfig(c: Config) -> bool:
    validateName(c.App.Name)
    validateKafka(c.Kafka)
    # validateSecret(c.Secret)
    return True
