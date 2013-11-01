"""Plugin framework.

Plugins are objects that configures and coordinates conversion machinery.
"""

import pkg_resources


def get_plugin(name, ui, settings):
    plugins = list(pkg_resources.iter_entry_points('ofxstatement', name))
    if not plugins:
        raise PluginNotRegistered(name)
    if len(plugins) > 1:
        raise PluginNameConflict(plugins)
    pcls = plugins[0].load()
    plugin = pcls(ui, settings)
    return plugin


def list_plugins():
    """Return list of all plugin classes registered as a list of tuples:

        [(name, plugin_class)]
    """
    plugin_eps = pkg_resources.iter_entry_points('ofxstatement')
    return sorted((ep.name, ep.load()) for ep in plugin_eps)


class PluginNotRegistered(Exception):
    """Raised on attempt to get plugin, missing from the registry.
    """


class PluginNameConflict(Exception):
    """Raised when there are more than one plugins registered with the same
    name
    """


class Plugin(object):
    ui = None

    def __init__(self, ui, settings):
        self.ui = ui
        self.settings = settings

    def get_parser(self, filename):
        raise NotImplementedError()
