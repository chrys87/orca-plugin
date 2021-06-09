import gi
gi.require_version('Peas', '1.0')
from gi.repository import GObject
from gi.repository import Peas
import time

class ByeOrca(GObject.Object, Peas.Activatable):
    #__gtype_name__ = 'ByeOrca'

    object = GObject.Property(type=GObject.Object)
    def __init__(self):
        pass
    def do_activate(self):
        API = self.object
        API.app.connectSignal("completed-application-stop", self.process)
    def do_deactivate(self):
        API = self.object
        API.app.disconnectSignalByFunction(self.process)
    def do_update_state(self):
        API = self.object
    def process(self, app):
        messages = app.getAPI('Messages')
        #app.getOrcaAPI('OrcaState').activeScript.presentMessage(messages.STOP_ORCA, resetStyles=False)
        app.getAPIHelper().outputMessage(messages.STOP_ORCA)

