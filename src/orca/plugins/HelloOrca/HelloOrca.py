from orca import plugin

import gi
gi.require_version('Peas', '1.0')
from gi.repository import GObject
from gi.repository import Peas

class HelloOrca(GObject.Object, Peas.Activatable, plugin.Plugin):
    #__gtype_name__ = 'HelloOrca'

    object = GObject.Property(type=GObject.Object)
    def __init__(self):
        plugin.Plugin.__init__(self)
    def do_activate(self):
        API = self.object
        self.connectSignal("start-application-completed", self.process)
    def do_deactivate(self):
        API = self.object
    def do_update_state(self):
        API = self.object
    def process(self, app):
        messages = app.getDynamicApiManager().getAPI('Messages')
        app.getDynamicApiManager().getAPI('OrcaState').activeScript.presentMessage(messages.START_ORCA, resetStyles=False)
