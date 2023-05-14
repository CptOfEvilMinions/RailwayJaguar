from pkg.config.load import (
    validateName,
    validateKafka,
    validateSecret,
    VerifyConfig,
    ReadConfig,
    Kafka,
    Secret,
)


def test_validateName():
    assert validateName("test") is True
    assert validateName("test1") is True
    assert validateName("test123") is True


def test_negativeValidateName():
    assert validateName("test-1") is not True
    assert validateName("test*1") is not True
    assert validateName("test_123") is not True


def test_validateKafka():
    k = Kafka(BoostrapServers=["127.0.0.1:9092"])
    assert validateKafka(k) is True

    k = Kafka(BoostrapServers=["127.0.0.1:9092", "127.0.1.1:9092"])
    assert validateKafka(k) is True


def test_validateSecret():
    s = Secret(
        VaultAddr="https://127.0.0.1:8200",
        # https://developer.hashicorp.com/vault/tutorials/tokens/tokens#tokens-with-use-limit
        VaultToken="hvs.CAESIJRM-T1q5lEjIWux1Tjx-VGqAYJdd4FZtbp1wpD5Ym9pGh4KHGh2cy5TSjRndGoxaU44NzNscm5MSlRLQXZ0ZGg",
    )
    assert validateSecret(s) is True


def test_verifyConfig():
    config = ReadConfig("tests/conf/server.yaml")
    assert VerifyConfig(config)


def test_ReadConfig(filePath: str):
    config = ReadConfig("tests/conf/server.yaml")
    assert config.App.Name == "test"
    assert config.Kafka.BoostrapServers[0] == "kafka.test:9092"
    assert config.Secret.VaultAddr == "https://vault.test:8200"
    assert config.Secret.VaultToken.startswith("hvs.CAESIJRM") is True
