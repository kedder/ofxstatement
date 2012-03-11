"""Plugin framework.

Plugins are objects that configures and coordinates conversion machinery.
"""


class Registry(object):
    """Registry of plugin classes
    """
    __plugins = {}

    def register(self, name, pluginCls):
        if name in self.__plugins:
            raise PluginAlreadyRegistered("%s: %s" % (name, self.get(name)))
        self.__plugins[name] = pluginCls

    def get(self, name):
        if name not in self.__plugins:
            raise PluginNotRegistered(name)
        return self.__plugins[name]

    def clear(self):
        self.__plugins = {}

    def enumerate(self):
        """Return list of pairs: (name, cls)
        """
        return self.__plugins.items()

registry = Registry()

def get_plugin(name, ui, settings):
    pcls = registry.get(name)
    plugin = pcls(ui, settings)
    return plugin

class PluginAlreadyRegistered(Exception):
    """Raised on attpemt to register an already registered plugin
    """

class PluginNotRegistered(Exception):
    """Raised on attempt to get plugin, missing from the registry.
    """

class Autoregisterable(type):
    def __init__(cls, name, bases, dict):
        pname = dict.get('name', None)
        if pname:
            registry.register(pname, cls)


class Plugin(metaclass=Autoregisterable):
    ui = None
    settings = None

    def __init__(self, ui, settings):
        self.ui = ui
        self.settings = settings

    def get_parser(self, filename):
        raise NotImplementedError()
