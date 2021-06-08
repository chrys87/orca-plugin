import gi, time
gi.require_version('Peas', '1.0')
from gi.repository import GObject
from gi.repository import Peas

class Time(GObject.Object, Peas.Activatable):
    #__gtype_name__ = 'Time'

    object = GObject.Property(type=GObject.Object)
    def __init__(self):
        self.keybinding = None
    def do_activate(self):
        API = self.object
        API.app.connectSignal("application-start-complete", self.setupCompatBinding)
        #self.setKeybinding('t')
    def setupCompatBinding(self, app):
        cmdnames = app.getAPI('Cmdnames')
        script_manager = app.getAPI('ScriptManager')
        _script_manager = script_manager.getManager()
        _script_manager._defaultScript.inputEventHandlers['presentTimeHandler'] = app.getAPIHelper().createInputEventHandler(self.presentTime, cmdnames.PRESENT_CURRENT_TIME)
        print('reg')
    def do_deactivate(self):
        API = self.object
        API.app.disconnectSignalByFunction(self.setupCompatBinding)

        #self.setKeybinding(None)
    def do_update_state(self):
        API = self.object
    def setKeybinding(self, keybinding):
        API = self.object
        #script = API.app.getOrcaAPI('OrcaState').activeScript
        #handler = API.app.getAPIHelper().createInputEventHandler(self.presentTime, cmdnames.PRESENT_CURRENT_TIME)
        #script.inputEventHandlers["presentTimeHandler"] = handler
        #script.inputEventHandlers.update(notification_messages.inputEventHandlers)
        #settings_manager = API.app.getOrcaAPI('SettingsManager')
        #_settingsManager = settings_manager.getManager()
        #print(_settingsManager.keybindings)
        #print(script.getKeyBindings())
        if keybinding == None:
            API.app.getAPIHelper().unregisterShortcut(self.keybinding)
        else:
            cmdnames = API.app.getAPI('Cmdnames')
            API.app.getAPIHelper().registerShortcut(self.presentTime, keybinding, cmdnames.PRESENT_CURRENT_TIME, clickCount = 1)
        self.keybinding = keybinding
        
    def presentTime(self, script, inputEvent):
        """ Presents the current time. """
        API = self.object
        settings_manager = API.app.getAPI('SettingsManager')
        _settingsManager = settings_manager.getManager()
        timeFormat = _settingsManager.getSetting('presentTimeFormat')
        message = time.strftime(timeFormat, time.localtime())
        API.app.getAPIHelper().outputMessage(message)
