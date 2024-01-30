from pkg.outputs.loader import LoadPlugins, CheckOutputs
from pkg.rules.load import Rule
from unittest.mock import patch
import unittest
import logging


class TestLoadPlugin(unittest.TestCase):
    def test_loadPlugins(self):
        logger = logging.Logger(name="test_loadPlugins")
        with patch("pkg.outputs.loader.__PLUGIN_DIR", "tests/plugins/[!__init__]*.py"):
            plugins = LoadPlugins(logger)

        self.assertEqual("example", list(plugins.keys())[0])

    def test_checkOutputs(self):
        logger = logging.Logger(name="test_loadPlugins")
        with patch("pkg.outputs.loader.__PLUGIN_DIR", "tests/plugins/[!__init__]*.py"):
            plugins = LoadPlugins(logger)
        rule: Rule = Rule("tests/rules/powershell_empire.yml")

        self.assertIsNone(CheckOutputs([rule], plugins))
