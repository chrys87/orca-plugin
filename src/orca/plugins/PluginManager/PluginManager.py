from orca import plugin

import gi
gi.require_version('Peas', '1.0')
from gi.repository import GObject
from gi.repository import Peas

import PluginManagerUi

class PluginManager(GObject.Object, Peas.Activatable, plugin.Plugin):
    #__gtype_name__ = 'PluginManager'

    object = GObject.Property(type=GObject.Object)
    def __init__(self):
        plugin.Plugin.__init__(self)
        self.pluginManagerUi = None
    def do_activate(self):
        API = self.object
        self.registerGestureByString(self.startPluginManagerUi, _('plugin manager'), 'kb:orca+e')

    def do_deactivate(self):
        API = self.object

    def startPluginManagerUi(self, script, inputEvent):
        self.showUI()
    def showUI(self):
        API = self.object
        if self.pluginManagerUi == None:
            self.pluginManagerUi = PluginManagerUi.PluginManagerUi(API.app)
            self.pluginManagerUi.setTranslationContext(self.getTranslationContext())
            self.pluginManagerUi.createUI()
            self.pluginManagerUi.run()
            self.pluginManagerUi = None
        else:
            self.pluginManagerUi.present()
