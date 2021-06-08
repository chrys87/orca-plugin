import gi, time
gi.require_version('Peas', '1.0')
from gi.repository import GObject
from gi.repository import Peas

class Date(GObject.Object, Peas.Activatable):
    #__gtype_name__ = 'Date'

    object = GObject.Property(type=GObject.Object)
    def __init__(self):
        self.keybinding = None
    def do_activate(self):
        API = self.object
        self.setKeybinding('t')
    def do_deactivate(self):
        API = self.object
        self.setKeybinding(None)
    def do_update_state(self):
        API = self.object
    def setKeybinding(self, keybinding):
        API = self.object
        if keybinding == None:
            API.app.getAPIHelper().unregisterShortcut(self.keybinding)
        else:
            cmdnames = API.app.getAPI('Cmdnames')
            API.app.getAPIHelper().registerShortcut(self.presentDate, keybinding, cmdnames.PRESENT_CURRENT_DATE, clickCount = 2)
        self.keybinding = keybinding
    def presentDate(self, script, inputEvent):
        """ Presents the current time. """
        API = self.object
        settings_manager = API.app.getAPI('SettingsManager')
        _settingsManager = settings_manager.getManager()
        dateFormat = _settingsManager.getSetting('presentDateFormat')
        message = time.strftime(dateFormat, time.localtime())
        API.app.getAPIHelper().outputMessage(message)
