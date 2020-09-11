"""Plugin framework.

Plugins are objects that configures and coordinates conversion machinery.
"""
from typing import List, Tuple, Type
from collections.abc import MutableMapping
import pkg_resources

from ofxstatement.ui import UI
from ofxstatement.parser import AbstractStatementParser


def get_plugin(name: str, ui: UI, settings: MutableMapping) -> "Plugin":
    plugins = list(pkg_resources.iter_entry_points("ofxstatement", name))
    if not plugins:
        raise PluginNotRegistered(name)
    if len(plugins) > 1:
        raise PluginNameConflict(plugins)
    pcls = plugins[0].load()
    plugin = pcls(ui, settings)
    return plugin


def list_plugins() -> List[Tuple[str, Type["Plugin"]]]:
    """Return list of all plugin classes registered as a list of tuples:

    [(name, plugin_class)]
    """
    plugin_eps = pkg_resources.iter_entry_points("ofxstatement")
    return sorted((ep.name, ep.load()) for ep in plugin_eps)


class PluginNotRegistered(Exception):
    """Raised on attempt to get plugin, missing from the registry."""


class PluginNameConflict(Exception):
    """Raised when there are more than one plugins registered with the same
    name
    """


class Plugin:
    ui: UI

    def __init__(self, ui: UI, settings: MutableMapping) -> None:
        self.ui = ui
        self.settings = settings

    def get_parser(self, filename: str) -> AbstractStatementParser:
        raise NotImplementedError()
