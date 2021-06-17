import gi
gi.require_version('Peas', '1.0')
from gi.repository import GObject
from gi.repository import Peas

import PluginManagerUi

class PluginManager(GObject.Object, Peas.Activatable):
    #__gtype_name__ = 'PluginManager'

    object = GObject.Property(type=GObject.Object)
    def __init__(self):
        self.keybinding = None
    def do_activate(self):
        API = self.object
        self.setKeybinding('e')
    def do_deactivate(self):
        API = self.object
        self.setKeybinding(None)

    def setKeybinding(self, keybinding):
        API = self.object
        if keybinding == None:
            API.app.getAPIHelper().unregisterShortcut(self.keybinding)
        else:
            API.app.getAPIHelper().registerShortcut(self.startPluginManagerUi, keybinding, 'plugin manager')
        self.keybinding = keybinding
    def startPluginManagerUi(self, script, inputEvent):
        self.showUI()

    def showUI(self):
        API = self.object
        pluginManagerUi = PluginManagerUi.PluginManagerUi()
        pluginList = API.app.getPluginSystemManager().plugins
        for plugin in pluginList:
            name = plugin.get_module_name()
            isActive = API.app.getPluginSystemManager().isPluginActive(plugin)
            pluginManagerUi.addPlugin(name, isActive)
        pluginManagerUi.run()
