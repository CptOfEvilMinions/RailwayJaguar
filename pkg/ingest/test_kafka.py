from pkg.ingest.kafka import CheckTopics, KafaTopic
from typing import List

import unittest


class TestKafka(unittest.TestCase):
    def test_checkTopics(self):
        ruleTopics: List[str] = [
            "zeek_conn",
            "zeek_dns",
            "zeek_files",
        ]
        kafkaTopics: List[str] = [
            "zeek_conn",
            "zeek_dns",
            "zeek_files",
        ]
        self.assertIsNone(CheckTopics(kafkaTopics, ruleTopics))

    def test_negativeCheckTopics(self):
        ruleTopics: List[str] = [
            "zeek_conn",
            "zeek_dns",
            "zeek_files",
        ]
        kafkaTopics: List[str] = [
            "zeek_dns",
            "zeek_files",
        ]

        with self.assertRaises(KafaTopic):
            CheckTopics(kafkaTopics, ruleTopics)
