import gi, time
gi.require_version('Peas', '1.0')
from gi.repository import GObject
from gi.repository import Peas

class Date(GObject.Object, Peas.Activatable):
    #__gtype_name__ = 'Date'

    object = GObject.Property(type=GObject.Object)
    def __init__(self):
        pass
    def do_activate(self):
        API = self.object
        API.app.signalManager.connectSignal("setup-inputeventhandlers-completed", self.setupCompatBinding)
    def setupCompatBinding(self, app):
        cmdnames = app.getAPI('Cmdnames')
        inputEventHandlers = app.getAPI('inputEventHandlers')
        inputEventHandlers['presentDateHandler'] = app.getAPIHelper().createInputEventHandler(self.presentDate, cmdnames.PRESENT_CURRENT_DATE)
    def do_deactivate(self):
        API = self.object
        API.app.signalManager.disconnectSignalByFunction(self.setupCompatBinding)
    def presentDate(self, script, inputEvent):
        """ Presents the current time. """
        API = self.object
        settings_manager = API.app.getAPI('SettingsManager')
        _settingsManager = settings_manager.getManager()
        dateFormat = _settingsManager.getSetting('presentDateFormat')
        message = time.strftime(dateFormat, time.localtime())
        API.app.getAPI('OrcaState').activeScript.presentMessage(message, resetStyles=False)


