#!/bin/python
"""PluginManager for loading orca plugins."""
import os, inspect, sys, pyatspi, tarfile, shutil

from enum import IntEnum
from gettext import gettext as _

version = sys.version[:3] # we only need major.minor version.
if version in ["3.3","3.4"]:
    from importlib.machinery import SourceFileLoader
else: # Python 3.5+, no support for python < 3.3.
    import importlib.util

import gi
gi.require_version('Peas', '1.0')
from gi.repository import GObject
from gi.repository import Peas


class API(GObject.GObject):
    """Interface that gives access to all the objects of Orca."""
    def __init__(self, app):
        GObject.GObject.__init__(self)
        self.app = app

class PluginType(IntEnum):
    """Types of plugins we support, depending on their directory location."""
    # pylint: disable=comparison-with-callable,inconsistent-return-statements,no-else-return
    
    # CORE: provides basic functionality
    # uninstallable: no
    # deactivateable: no
    CORE = 1
    # SYSTEM: provides system wide plugins
    # uninstallable: no
    # deactivateable: yes
    SYSTEM = 2
    # USER: provides per user plugin
    # uninstallable: yes
    # deactivateable: yes
    USER = 3

    def __str__(self):
        if self.value == PluginType.CORE:
            return _("Core plugin")
        elif self.value == PluginType.SYSTEM:
            return _("System plugin")
        elif self.value == PluginType.USER:
            return _("User plugin")

    def get_root_dir(self):
        """Returns the directory where this type of plugins can be found."""
        if self.value == PluginType.CORE:
            return os.path.dirname(os.path.realpath(os.path.abspath(inspect.getfile(inspect.currentframe())))) + '/core-plugins'
        elif self.value == PluginType.SYSTEM:
            return os.path.dirname(os.path.realpath(os.path.abspath(inspect.getfile(inspect.currentframe())))) + '/plugins'
        elif self.value == PluginType.USER:
            return os.path.expanduser('~') + '/.local/share/orca/plugins'


class PluginSystemManager():
    """Orca Plugin Manager to handle a set of plugins.
    Attributes:
        DEFAULT_LOADERS (tuple): Default loaders used by the plugin manager. For
            possible values see
            https://developer.gnome.org/libpeas/stable/PeasEngine.html#peas-engine-enable-loader
    """
    DEFAULT_LOADERS = ("python3", )

    def __init__(self, app):
        self.app = app
        self.engine = Peas.Engine.get_default()

        for loader in self.DEFAULT_LOADERS:
            self.engine.enable_loader(loader)

        self._setupPluginsDir()
        self._setup_extension_set()
        self._activePlugins = ['HelloOrca','ByeOrca', 'SelfVoice', 'Hello', 'Date', 'MouseReview', 'ClassicPreferences', ' PluginManager']
    @property
    def plugins(self):
        """Gets the engine's plugin list."""
        return self.engine.get_plugin_list()

    @classmethod
    def getPluginType(cls, plugin_info):
        """Gets the PluginType for the specified Peas.PluginInfo."""
        paths = [plugin_info.get_data_dir(), PluginType.CORE.get_root_dir()]
        if os.path.commonprefix(paths) == PluginType.CORE.get_root_dir():
            return PluginType.CORE
        paths = [plugin_info.get_data_dir(), PluginType.SYSTEM.get_root_dir()]
        if os.path.commonprefix(paths) == PluginType.SYSTEM.get_root_dir():
            return PluginType.SYSTEM
        return PluginType.USER

    def get_extension(self, pluginName):
        """Gets the extension identified by the specified name.
        Args:
            pluginName (str): The name of the extension.
        Returns:
            The extension if exists. Otherwise, `None`.
        """
        plugin = self.getPluginInfoByName(pluginName)
        if not plugin:
            return None

        return self.extension_set.get_extension(plugin)
    def rescanPlugins(self):
        self.engine.garbage_collect()
        self.engine.rescan_plugins()
    def getPluginInfoByName(self, pluginName, pluginType=PluginType.USER):
        """Gets the plugin info for the specified plugin name.
        Args:
            pluginName (str): The name from the .plugin file of the module.
        Returns:
            Peas.PluginInfo: The plugin info if it exists. Otherwise, `None`.
        """
        for plugin in self.plugins:
            if plugin.get_module_name() == pluginName:
                return plugin
        return None
    def getActivePlugins(self):
        return self._activePlugins
    def setPluginActive(self, pluginName, active):
        if active:
            if not pluginName in self.getActivePlugins():
                self._activePlugins.append(pluginName)
        else:
            if pluginName in self.getActivePlugins():
                self._activePlugins.remove(pluginName)
    def isPluginNameActive(self, pluginName):
        plugin_info = self.engine.get_plugin_info(pluginName)
        self.isPluginActive(plugin_info)
    def isPluginActive(self, pluginInfo):
        # TODO: currently all plugins are active, so settings infra yet
        #return True
        if PluginSystemManager.getPluginType(pluginInfo) == PluginType.CORE:
            return True
        active_plugin_names = self.getActivePlugins()
        return pluginInfo.get_module_name() in active_plugin_names
    def syncAllPluginsActive(self, ForceAllPlugins=False):
        self.unloadAllPlugins(ForceAllPlugins)
        self.loadAllPlugins(ForceAllPlugins)

    def loadAllPlugins(self, ForceAllPlugins=False):
        """Loads plugins from settings."""
        active_plugin_names = self.getActivePlugins()
        for plugin in self.plugins:
            if self.isPluginActive(plugin) or ForceAllPlugins:
                self.loadPlugin(plugin.get_module_name())

    def loadPlugin(self, plugin_name):
        try:
            plugin_info = self.engine.get_plugin_info(plugin_name)
            if plugin_info not in self.plugins:
                print("Plugin missing: {}".format(plugin_name))
                return
            self.engine.load_plugin(plugin_info)
        except e as Exception:
            print(e)

    def unloadAllPlugins(self, ForceAllPlugins=False):
        """Loads plugins from settings."""
        active_plugin_names = self.getActivePlugins()
        for plugin in self.plugins:
            if not self.isPluginActive(plugin) or ForceAllPlugins:
                self.unloadPlugin(plugin.get_module_name())

    def unloadPlugin(self, plugin_name):
        try:
            plugin_info = self.engine.get_plugin_info(plugin_name)
            if plugin_info not in self.plugins:
                print("Plugin missing: {}".format(plugin_name))
                return
            if PluginSystemManager.getPluginType(plugin_info) == PluginType.CORE:
                return
            self.engine.unload_plugin(plugin_info)
        except e as Exception:
            print(e)
    def installPlugin(self, pluginFilePath, pluginType=PluginType.USER):
        if not self.isValidPluginFile(pluginFilePath):
            return False
        pluginFolder = pluginType.get_root_dir()
        if not pluginFolder.endswith('/'):
            pluginFolder += '/'
        if not os.path.exists(pluginFolder):
            os.mkdir(pluginFolder)
        else:
            if not os.path.isdir(pluginFolder):
                return False

        try:
            with tarfile.open(pluginFilePath) as tar:
                tar.extractall(path=pluginFolder)
        except Exception as e:
            print(e)
        print('install', pluginFilePath)
        self.rescanPlugins()
        return True
    def isValidPluginFile(self, pluginFilePath):
        if not isinstance(pluginFilePath, str):
            return False
        if pluginFilePath == '':
            return False
        if not os.path.exists(pluginFilePath):
            return False
        pluginFolder = ''
        pluginFileExists = False
        try:
            with tarfile.open(pluginFilePath) as tar:
                tarMembers = tar.getmembers()
                for tarMember in tarMembers:
                    if tarMember.isdir():
                        if pluginFolder == '':
                            pluginFolder = tarMember.name
                    if tarMember.isfile():
                        if tarMember.name.endswith('.plugin'):
                            pluginFileExists = True
                    if not tarMember.name.startswith(pluginFolder):
                        print(pluginFolder, tarMember.name)
                        return False
        except Exception as e:
            print(e)
            return False
        return pluginFileExists
    def uninstallPlugin(self, pluginName, pluginType=PluginType.USER):
        pluginFolder = pluginType.get_root_dir()
        if not pluginFolder.endswith('/'):
            pluginFolder += '/'
        if not os.path.isdir(pluginFolder):
            return False
        if not os.path.isdir(pluginFolder + pluginName):
            return False
        if self.isPluginActive(pluginName):
            self.unloadPlugin(pluginName)
        try:
            shutil.rmtree(pluginFolder + pluginName, ignore_errors=True)
        except Exception as e:
            print(e)
            return False
        self.rescanPlugins()
        return True
    def _setup_extension_set(self):
        plugin_iface = API(self.app)
        self.extension_set = Peas.ExtensionSet.new(self.engine,
                                                   Peas.Activatable,
                                                   ["object"],
                                                   [plugin_iface])
        self.extension_set.connect("extension-removed",
                                   self.__extension_removed_cb)
        self.extension_set.connect("extension-added",
                                   self.__extension_added_cb)

    def _setupPluginsDir(self):
        core_plugins_dir = PluginType.CORE.get_root_dir()
        system_plugins_dir = PluginType.SYSTEM.get_root_dir()
        user_plugins_dir = PluginType.USER.get_root_dir()
        if os.path.exists(user_plugins_dir):
            self.engine.add_search_path(user_plugins_dir)
        if os.path.exists(system_plugins_dir):
            self.engine.add_search_path(system_plugins_dir)
        if os.path.exists(core_plugins_dir):
            self.engine.add_search_path(core_plugins_dir)

    @staticmethod
    def __extension_removed_cb(unused_set, unused_plugin_info, extension):
        extension.deactivate()

    @staticmethod
    def __extension_added_cb(unused_set, unused_plugin_info, extension):
        extension.activate()

    def __loaded_plugins_cb(self, engine, unused_pspec):
        """Handles the changing of the loaded plugin list."""
        self.app.settings.ActivePlugins = engine.get_property("loaded-plugins")

class APIHelper():
    def __init__(self, app):
        self.app = app
        self.orcaKeyBindings = None

    '''
    _pluginAPIManager.setOrcaAPI('Logger', _logger)
    _pluginAPIManager.setOrcaAPI('SettingsManager', _settingsManager)
    _pluginAPIManager.setOrcaAPI('ScriptManager', _scriptManager)
    _pluginAPIManager.setOrcaAPI('EventManager', _eventManager)
    _pluginAPIManager.setOrcaAPI('Speech', speech)
    _pluginAPIManager.setOrcaAPI('Sound', sound)
    _pluginAPIManager.setOrcaAPI('Braille', braille)
    _pluginAPIManager.setOrcaAPI('Debug', debug)
    _pluginAPIManager.setOrcaAPI('Messages', messages)
    _pluginAPIManager.setOrcaAPI('MouseReview', mouse_review)
    _pluginAPIManager.setOrcaAPI('NotificationMessages', notification_messages)
    _pluginAPIManager.setOrcaAPI('OrcaState', orca_state)
    _pluginAPIManager.setOrcaAPI('OrcaPlatform', orca_platform)
    _pluginAPIManager.setOrcaAPI('OrcaPlatform', orca_platform)
    _pluginAPIManager.setOrcaAPI('Settings', settings)
    _pluginAPIManager.setOrcaAPI('Keybindings', keybindings)
    '''
    def outputMessage(self, Message, interrupt=False):
        settings = self.app.getDynamicApiManager().getAPI('Settings')
        braille = self.app.getDynamicApiManager().getAPI('Braille')
        speech = self.app.getDynamicApiManager().getAPI('Speech')
        if speech != None:
            if (settings.enableSpeech):
                if interrupt:
                    speech.cancel()
                if Message != '':
                    speech.speak(Message)
        if braille != None:
            if (settings.enableBraille):
                braille.displayMessage(Message)
    def createInputEventHandler(self, function, name, learnModeEnabled=True):
        EventManager = self.app.getDynamicApiManager().getAPI('EventManager')
        newInputEventHandler = EventManager.input_event.InputEventHandler(function, name, learnModeEnabled)
        return newInputEventHandler
    def registerGestureByString(self, function, name, gestureString, learnModeEnabled = True):
        gestureList = gestureString.split(',')
        registeredGestures = []
        for gesture in gestureList:
            if gesture.startswith('kb:'):
                shortcutString = gesture[3:]
                registuredGesture = self.registerShortcutByString(function, name, shortcutString, learnModeEnabled)
                if registuredGesture:
                    registeredGestures.append(registuredGesture)
        return registeredGestures
    def registerShortcutByString(self, function, name, shortcutString, learnModeEnabled = True):
        clickCount = 0
        orcaKey = False
        shiftKey = False
        ctrlKey = False
        altKey = False
        key = ''
        shortcutList = shortcutString.split('+')
        for shortcutElement in shortcutList:
            shortcutElementLower = shortcutElement.lower()
            if shortcutElementLower == 'press':
                clickCount += 1
            elif shortcutElement == 'orca':
                orcaKey = True
            elif shortcutElementLower == 'shift':
                shiftKey = True
            elif shortcutElementLower == 'control':
                ctrlKey = True
            elif shortcutElementLower == 'alt':
                altKey = True
            else:
                key = shortcutElementLower
        if clickCount == 0:
            clickCount = 1
        return self.registerShortcut(function, key, name, clickCount, orcaKey, shiftKey, ctrlKey, altKey, learnModeEnabled)

    def registerShortcut(self, function, key, name, clickCount = 1, orcaKey = True, shiftKey = False, ctrlKey = False, altKey = False, learnModeEnabled = True):
        keybindings = self.app.getDynamicApiManager().getAPI('Keybindings')
        settings = self.app.getDynamicApiManager().getAPI('Settings')

        if self.orcaKeyBindings == None:
            self.orcaKeyBindings = keybindings.KeyBindings()
        newInputEventHandler = self.createInputEventHandler(function, name, learnModeEnabled)

        currModifierMask = keybindings.NO_MODIFIER_MASK
        if orcaKey:
            currModifierMask = currModifierMask | 1 << keybindings.MODIFIER_ORCA
        if shiftKey:
            currModifierMask = currModifierMask | 1 << pyatspi.MODIFIER_SHIFT
        if altKey:
            currModifierMask = currModifierMask | 1 << pyatspi.MODIFIER_ALT
        if ctrlKey:
            currModifierMask = currModifierMask | 1 << pyatspi.MODIFIER_CONTROL

        newKeyBinding = keybindings.KeyBinding(key, keybindings.defaultModifierMask, currModifierMask, newInputEventHandler, clickCount)
        self.orcaKeyBindings.add(newKeyBinding)

        settings.keyBindingsMap["default"] = self.orcaKeyBindings
        print(settings.keyBindingsMap["default"])

        return newKeyBinding
    def unregisterShortcut(self, KeyBindingToRemove):
        print(KeyBindingToRemove)
        keybindings = self.app.getDynamicApiManager().getAPI('Keybindings')
        settings = self.app.getDynamicApiManager().getAPI('Settings')
        EventManager = self.app.getDynamicApiManager().getAPI('EventManager')
        
        if self.orcaKeyBindings == None:
            self.orcaKeyBindings = keybindings.KeyBindings()

        self.orcaKeyBindings.remove(KeyBindingToRemove)
        settings.keyBindingsMap["default"] = self.orcaKeyBindings
        print(settings.keyBindingsMap["default"])
    def importModule(self, moduleName, moduleLocation):
        if version in ["3.3","3.4"]:
            return SourceFileLoader(moduleName, moduleLocation).load_module()
        else:
            spec = importlib.util.spec_from_file_location(moduleName, moduleLocation)
            driver_mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(driver_mod)
            return driver_mod
