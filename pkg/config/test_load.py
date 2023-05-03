from pkg.config.load import (
    validateName,
    validateKafka,
    validateSecret,
    VerifyConfig,
    ReadConfig,
    Kafka,
    Secret
)

def test_validateName():
    assert validateName("test") is True
    assert validateName("test1") is True
    assert validateName("test123") is True

# def test_negativeValidateName():
#     assert validateName("test-1") is not True
#     assert validateName("test*1") is not True
#     assert validateName("test_123") is not True
    

# def test_validateKafka():
#     k = Kafka(
#         boostrap_servers=["127.0.0.1:9092"]
#     )
#     assert validateKafka(k) is True

#     k = Kafka(
#         boostrap_servers=["127.0.0.1:9092", "127.0.1.1:9092"]
#     )
#     assert validateKafka(k) is True


# def test_validateSecret():
#     s = Secret(
#         vault_addr="https://127.0.0.1:8200",
#         # https://developer.hashicorp.com/vault/tutorials/tokens/tokens#tokens-with-use-limit
#         vault_token="hvs.CAESIJRM-T1q5lEjIWux1Tjx-VGqAYJdd4FZtbp1wpD5Ym9pGh4KHGh2cy5TSjRndGoxaU44NzNscm5MSlRLQXZ0ZGg"
#     )
#     assert validateSecret(s) is True


# def test_verifyConfig():
#     config = ReadConfig("tests/conf/server.yaml")
#     assert VerifyConfig(config)


# def test_ReadConfig(filePath: str):
#     config = ReadConfig("tests/conf/server.yaml")
#     assert config.app.name == "test"
#     assert config.kafka.boostrap_servers[0] == "kafka.test:9092"
#     assert config.secret.vault_addr == "https://vault.test:8200"
#     assert config.secret.vault_token.startswith("hvs.CAESIJRM") is True

