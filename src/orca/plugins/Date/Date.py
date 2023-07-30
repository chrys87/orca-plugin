from orca import plugin

import gi, time
gi.require_version('Peas', '1.0')
from gi.repository import GObject
from gi.repository import Peas

class Date(GObject.Object, Peas.Activatable, plugin.Plugin):
    #__gtype_name__ = 'Date'

    object = GObject.Property(type=GObject.Object)
    def __init__(self):
        plugin.Plugin.__init__(self)
    def do_activate(self):
        API = self.object
        self.connectSignal("setup-inputeventhandlers-completed", self.setupCompatBinding)
    def setupCompatBinding(self, app):
        cmdnames = app.getDynamicApiManager().getAPI('Cmdnames')
        inputEventHandlers = app.getDynamicApiManager().getAPI('inputEventHandlers')
        inputEventHandlers['presentDateHandler'] = app.getAPIHelper().createInputEventHandler(self.presentDate, cmdnames.PRESENT_CURRENT_DATE)
    def do_deactivate(self):
        API = self.object
        inputEventHandlers = API.app.getDynamicApiManager().getAPI('inputEventHandlers')
        del inputEventHandlers['presentDateHandler']
    def presentDate(self, script=None, inputEvent=None):
        """ Presents the current time. """
        API = self.object
        settings_manager = API.app.getDynamicApiManager().getAPI('SettingsManager')
        _settingsManager = settings_manager.getManager()
        dateFormat = _settingsManager.getSetting('presentDateFormat')
        message = time.strftime(dateFormat, time.localtime())
        API.app.getDynamicApiManager().getAPI('OrcaState').activeScript.presentMessage(message, resetStyles=False)
        return True
