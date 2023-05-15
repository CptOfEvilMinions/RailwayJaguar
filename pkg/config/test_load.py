from pkg.config.load import (
    validateName,
    validateKafka,
    validateSecret,
    VerifyConfig,
    ReadConfig,
    Kafka,
    Secret,
    InvalidName,
    InvalidVaultSecret,
)
import unittest


class Test(unittest.TestCase):
    def test_validateName(self):
        self.assertTrue(validateName("test"))
        self.assertTrue(validateName("test1"))
        self.assertTrue(validateName("test123"))

    def test_negativeValidateName(self):
        with self.assertRaises(InvalidName):
            validateName("test-1")
            validateName("test*1")
            validateName("test_123")

    def test_validateKafka(self):
        k = Kafka(BoostrapServers=["127.0.0.1:9092"])
        self.assertTrue(validateKafka(k))

        k = Kafka(BoostrapServers=["127.0.0.1:9092", "127.0.1.1:9092"])
        self.assertTrue(validateKafka(k))

    def test_validateSecret(self):
        s = Secret(
            VaultAddr="https://127.0.0.1:8200",
            # https://developer.hashicorp.com/vault/tutorials/tokens/tokens#tokens-with-use-limit
            VaultToken="hvs.CAESIJRM-T1q5lEjIWux1Tjx-VGqAYJdd4FZtbp1wpD5Ym9pGh4KHGh2cy5TSjRndGoxaU44NzNscm5MSlRLQXZ0ZGg",  # noqa: E501
        )
        self.assertTrue(validateSecret(s))

    def test_negativeValidateSecret(self):
        s = Secret(
            VaultAddr="https://127.0.0.1:8200",
            # https://developer.hashicorp.com/vault/tutorials/tokens/tokens#tokens-with-use-limit
            VaultToken="abc123",
        )
        with self.assertRaises(InvalidVaultSecret):
            validateSecret(s)

    def test_verifyConfig(self):
        config = ReadConfig("tests/conf/server.yml")
        self.assertTrue(VerifyConfig(config))

    def test_ReadConfig(self):
        config = ReadConfig("tests/conf/server.yml")
        self.assertEqual(config.App.Name, "test")
        self.assertEqual(
            config.Kafka.BoostrapServers,
            ["kafka.hackinglab.local:9092", "broker:29092"],
        )
        self.assertEqual(config.Secret.VaultAddr, "https://vault.test:8200")
        self.assertTrue(config.Secret.VaultToken.startswith("hvs.CAESIJRM"))
