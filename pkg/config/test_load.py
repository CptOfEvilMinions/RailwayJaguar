from pkg.config.load import (
    validateName,
    validateKafka,
    VerifyConfig,
    ReadConfig,
    Kafka,
    InvalidName,
)
import unittest


class TestConfigValidators(unittest.TestCase):
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
