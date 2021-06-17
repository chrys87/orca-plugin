import gi
gi.require_version('Peas', '1.0')
from gi.repository import GObject
from gi.repository import Peas

class HelloOrca(GObject.Object, Peas.Activatable):
    #__gtype_name__ = 'HelloOrca'

    object = GObject.Property(type=GObject.Object)
    def __init__(self):
        pass
    def do_activate(self):
        API = self.object
        API.app.getSignalManager().connectSignal("start-application-completed", self.process)
    def do_deactivate(self):
        API = self.object
        API.app.getSignalManager().disconnectSignalByFunction(self.process)
    def do_update_state(self):
        API = self.object
    def process(self, app):
        messages = app.getDynamicApiManager().getAPI('Messages')
        app.getDynamicApiManager().getAPI('OrcaState').activeScript.presentMessage(messages.START_ORCA, resetStyles=False)
