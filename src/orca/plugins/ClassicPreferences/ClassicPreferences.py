from orca import plugin

import gi, time
gi.require_version('Peas', '1.0')
from gi.repository import GObject
from gi.repository import Peas
import importlib, os
import orca_gui_prefs

class ClassicPreferences(GObject.Object, Peas.Activatable, plugin.Plugin):
    #__gtype_name__ = 'ClassicPreferences'

    object = GObject.Property(type=GObject.Object)
    def __init__(self):
        plugin.Plugin.__init__(self)
    def do_activate(self):
        API = self.object
        self.connectSignal("setup-inputeventhandlers-completed", self.setupCompatBinding)
        #self.setupCompatBinding(API.app)
    def setupCompatBinding(self, app):
        cmdnames = app.getDynamicApiManager().getAPI('Cmdnames')
        inputEventHandlers = app.getDynamicApiManager().getAPI('inputEventHandlers')
        inputEventHandlers['preferencesSettingsHandler'] = app.getAPIHelper().createInputEventHandler(self.showPreferencesGUI, cmdnames.SHOW_PREFERENCES_GUI)
        inputEventHandlers['appPreferencesSettingsHandler'] = app.getAPIHelper().createInputEventHandler(self.showAppPreferencesGUI, cmdnames.SHOW_APP_PREFERENCES_GUI)
    def do_deactivate(self):
        API = self.object
        inputEventHandlers = API.app.getDynamicApiManager().getAPI('inputEventHandlers')
        del inputEventHandlers['preferencesSettingsHandler']
        del inputEventHandlers['appPreferencesSettingsHandler']
    def do_update_state(self):
        API = self.object
    def showAppPreferencesGUI(self, script=None, inputEvent=None):
        """Displays the user interface to configure the settings for a
        specific applications within Orca and set up those app-specific
        user preferences using a GUI.

        Returns True to indicate the input event has been consumed.
        """
        API = self.object
        orca_state = API.app.getDynamicApiManager().getAPI('OrcaState')
        settings = API.app.getDynamicApiManager().getAPI('Settings')
        _settingsManager = API.app.getDynamicApiManager().getAPI('SettingsManager').getManager()
        _scriptManager = API.app.getDynamicApiManager().getAPI('ScriptManager').getManager()

        prefs = {}
        for key in settings.userCustomizableSettings:
            prefs[key] = _settingsManager.getSetting(key)

        script = script or orca_state.activeScript
        self._showPreferencesUI(script, prefs)
        return True
    def showPreferencesGUI(self, script=None, inputEvent=None):
        """Displays the user interface to configure Orca and set up
        user preferences using a GUI.

        Returns True to indicate the input event has been consumed.
        """
        API = self.object
        orca_state = API.app.getDynamicApiManager().getAPI('OrcaState')
        settings = API.app.getDynamicApiManager().getAPI('Settings')
        _settingsManager = API.app.getDynamicApiManager().getAPI('SettingsManager').getManager()
        _scriptManager = API.app.getDynamicApiManager().getAPI('ScriptManager').getManager()
        debug = API.app.getDynamicApiManager().getAPI('Debug')
        prefs = _settingsManager.getGeneralSettings(_settingsManager.profile)
        script = _scriptManager.getDefaultScript()
        self._showPreferencesUI(script, prefs)
        return True
    def _showPreferencesUI(self, script, prefs):
        API = self.object
        orca_state = API.app.getDynamicApiManager().getAPI('OrcaState')
        debug = API.app.getDynamicApiManager().getAPI('Debug')
        orca_platform = API.app.getDynamicApiManager().getAPI('OrcaPlatform')
        
        if orca_state.orcaOS:
            orca_state.orcaOS.showGUI()
            return

        uiFile = os.path.join(orca_platform.datadir,
                            orca_platform.package,
                            "ui",
                            "orca-setup.ui")
        uiFile = os.path.join(self.getModuleDir(),
                            "ui",
                            "orca-setup.ui")
        orca_state.orcaOS = orca_gui_prefs.OrcaSetupGUI(uiFile, "orcaSetupWindow", prefs, API.app)
        orca_state.orcaOS.init(script)
        orca_state.orcaOS.setTranslationContext(self.getTranslationContext())
        orca_state.orcaOS.showGUI()
