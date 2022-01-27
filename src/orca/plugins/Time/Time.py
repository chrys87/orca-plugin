import gi, time
gi.require_version('Peas', '1.0')
from gi.repository import GObject
from gi.repository import Peas

from orca import plugin

class Time(GObject.Object, Peas.Activatable, plugin.Plugin):
    #__gtype_name__ = 'Time'

    object = GObject.Property(type=GObject.Object)
    def __init__(self):
        plugin.Plugin.__init__(self)
    def do_activate(self):
        API = self.object
        self.connectSignal("setup-inputeventhandlers-completed", self.setupCompatBinding)
    def setupCompatBinding(self, app):
        cmdnames = app.getDynamicApiManager().getAPI('Cmdnames')
        inputEventHandlers = app.getDynamicApiManager().getAPI('inputEventHandlers')
        inputEventHandlers['presentTimeHandler'] = app.getAPIHelper().createInputEventHandler(self.presentTime, cmdnames.PRESENT_CURRENT_TIME)
    def do_deactivate(self):
        API = self.object
        API.app.getSignalManager().disconnectSignalByFunction(self.setupCompatBinding)
        inputEventHandlers = API.app.getDynamicApiManager().getAPI('inputEventHandlers')
        del inputEventHandlers['presentTimeHandler']
        #API.app.getDynamicApiManager().registerAPI('inputEventHandlers', inputEventHandlers)
        inputEventHandlers = API.app.getDynamicApiManager().getAPI('inputEventHandlers')
    def do_update_state(self):
        API = self.object
    def presentTime(self, script, inputEvent):
        """ Presents the current time. """
        API = self.object
        settings_manager = API.app.getDynamicApiManager().getAPI('SettingsManager')
        _settingsManager = settings_manager.getManager()
        timeFormat = _settingsManager.getSetting('presentTimeFormat')
        message = time.strftime(timeFormat, time.localtime())
        API.app.getDynamicApiManager().getAPI('OrcaState').activeScript.presentMessage(message, resetStyles=False)
