from pkg.rules.yaml_checker import (
    validateVersion,
    validateKind,
    validatePythonRule,
    validateKafkaTopic,
    InvalidKind,
    InvalidVersion,
    InvalidPythonRule,
    InvalidKafkaTopic,
)
import unittest


class Test(unittest.TestCase):
    def test_validateKind(self):
        self.assertTrue(validateKind("stream_alert"))

    def test_negative_validateKind(self):
        with self.assertRaises(InvalidKind):
            validateKind("alert")

    def test_validateVersion(self):
        self.assertTrue(validateVersion("v1"))

    def test_negative_validateVersion(self):
        with self.assertRaises(InvalidVersion):
            validateVersion("a")
            validateVersion("1")
            validateVersion("1.0")
            validateVersion("vA")

    def test_validatePythonRule(self):
        self.assertTrue(validatePythonRule("hello.py"))

    def test_negative_validatePythonRule(self):
        with self.assertRaises(InvalidPythonRule):
            validatePythonRule("hello.c")

    def test_validateKafkaTopic(self):
        assert validateKafkaTopic("hello") is True

    def test_negative_validateKafkaTopic(self):
        with self.assertRaises(InvalidKafkaTopic):
            validateKafkaTopic("foor bar")
