from typing import Dict, Set, List
from pkg.rules.model import Rule
from types import ModuleType
import importlib
import logging
import glob

__PLUGIN_DIR: str = "plugins/[!__init__]*.py"


class OutputPluginDNE(Exception):
    def __init__(self, pluginName: set[str]):
        self.msg = f"Output plugin {pluginName} does not exist ."

    def __str__(self):
        return self.msg


def LoadPlugins(logger: logging.Logger) -> Dict[str, ModuleType]:
    """
    Load the plugins

    Return:
        discovered_plugins (Dict[str, ModuleType]): pluginName -> Module
    """

    plugins: Dict[str, ModuleType] = {}
    for path in glob.glob(__PLUGIN_DIR):
        try:
            # Load plugin
            modPath = path.removesuffix(".py").replace("/", ".")
            plugin = importlib.import_module(modPath).Plugin(logger)
            # Initialize plugin
            plugin.initialize()
        except Exception as exc:
            raise exc
        plugins[plugin.meta.name] = plugin
    return plugins


def CheckOutputs(rules: List[Rule], outputPlugins: Dict[str, ModuleType]) -> None:
    """
    Using the outputs defined in rule YAMLs, check to see that each
    reference has a loaded rule.

    Params:
        rules: (List[Rule]) - List of rules
        outputPlugins: (Dict[str, ModuleType]) - Dict of loaded plugins
    """
    rulePlugins: Set[str] = set()
    outputPluginsNames: Set[str] = set(outputPlugins.keys())

    for rule in rules:
        for plugin in rule.Metadata.Outputs:
            rulePlugins.add(plugin)

    if len(rulePlugins.difference(outputPluginsNames)) != 0:
        raise OutputPluginDNE(rulePlugins.difference(outputPluginsNames))
    return
