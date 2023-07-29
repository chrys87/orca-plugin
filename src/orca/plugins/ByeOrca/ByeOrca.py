from orca import plugin

import gi
gi.require_version('Peas', '1.0')
from gi.repository import GObject
from gi.repository import Peas
import time


class ByeOrca(GObject.Object, Peas.Activatable, plugin.Plugin):
    #__gtype_name__ = 'ByeOrca'

    object = GObject.Property(type=GObject.Object)
    def __init__(self):
        plugin.Plugin.__init__(self)
    def do_activate(self):
        API = self.object
        self.connectSignal("stop-application-completed", self.process)
    def do_deactivate(self):
        API = self.object
    def do_update_state(self):
        API = self.object
    def process(self, app):
        messages = app.getDynamicApiManager().getAPI('Messages')
        activeScript = app.getDynamicApiManager().getAPI('OrcaState').activeScript
        activeScript.presentationInterrupt()
        activeScript.presentMessage(messages.STOP_ORCA, resetStyles=False)
