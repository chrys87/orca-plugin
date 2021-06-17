import gi, time
gi.require_version('Peas', '1.0')
from gi.repository import GObject
from gi.repository import Peas

class Time(GObject.Object, Peas.Activatable):
    #__gtype_name__ = 'Time'

    object = GObject.Property(type=GObject.Object)
    def __init__(self):
        pass
    def do_activate(self):
        API = self.object
        API.app.signalManager.connectSignal("setup-inputeventhandlers-completed", self.setupCompatBinding)
    def setupCompatBinding(self, app):
        cmdnames = app.getAPI('Cmdnames')
        inputEventHandlers = app.getAPI('inputEventHandlers')
        inputEventHandlers['presentTimeHandler'] = app.getAPIHelper().createInputEventHandler(self.presentTime, cmdnames.PRESENT_CURRENT_TIME)
    def do_deactivate(self):
        API = self.object
        API.app.signalManager.disconnectSignalByFunction(self.setupCompatBinding)
    def do_update_state(self):
        API = self.object
    def presentTime(self, script, inputEvent):
        """ Presents the current time. """
        API = self.object
        settings_manager = API.app.getAPI('SettingsManager')
        _settingsManager = settings_manager.getManager()
        timeFormat = _settingsManager.getSetting('presentTimeFormat')
        message = time.strftime(timeFormat, time.localtime())
        API.app.getAPI('OrcaState').activeScript.presentMessage(message, resetStyles=False)
