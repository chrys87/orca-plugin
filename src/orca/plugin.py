import os, inspect
import gi
from gi.repository import GObject

class Plugin():
    #__gtype_name__ = 'BasePlugin'

    def __init__(self, *args, **kwargs):
        self.API = None
        self.pluginInfo = None
        self.moduleDir = ''
        self.hidden = False
        self.moduleName = ''
        self.name = ''
        self.version = ''
        self.website = ''
        self.authors = []
        self.buildIn = False
        self.description = ''
        self.iconName = ''
        self.copyright = ''
        self.dependencies = False
        self.helpUri = ''
        self.dataDir = ''
        self.translationContext = None
    def setApp(self, app):
        self.app = app
        self.dynamicApiManager = app.getDynamicApiManager()
        self.signalManager = app.getSignalManager()

    def getApp(self):
        return self.app
    def setPluginInfo(self, pluginInfo):
        self.pluginInfo = pluginInfo
        self.updatePluginInfoAttributes()
    def getPluginInfo(self):
        return self.pluginInfo
    def updatePluginInfoAttributes(self):
        self.moduleDir = ''
        self.hidden = False
        self.moduleName = ''
        self.name = ''
        self.version = ''
        self.website = ''
        self.authors = []
        self.buildIn = False
        self.description = ''
        self.iconName = ''
        self.copyright = ''
        self.dependencies = False
        self.helpUri = ''
        self.dataDir = ''
        pluginInfo = self.getPluginInfo()
        if pluginInfo == None:
            return
        self.moduleName = self.getApp().getPluginSystemManager().getPluginModuleName(pluginInfo)
        self.name = self.getApp().getPluginSystemManager().getPluginName(pluginInfo)
        self.version = self.getApp().getPluginSystemManager().getPluginVersion(pluginInfo)
        self.moduleDir = self.getApp().getPluginSystemManager().getPluginModuleDir(pluginInfo)
        self.buildIn = self.getApp().getPluginSystemManager().isPluginBuildIn(pluginInfo)
        self.description = self.getApp().getPluginSystemManager().getPluginDescription(pluginInfo)
        self.hidden = self.getApp().getPluginSystemManager().isPluginHidden(pluginInfo)
        self.website = self.getApp().getPluginSystemManager().getPluginWebsite(pluginInfo)
        self.authors = self.getApp().getPluginSystemManager().getPluginAuthors(pluginInfo)
        self.iconName = self.getApp().getPluginSystemManager().getPluginIconName(pluginInfo)
        self.copyright = self.getApp().getPluginSystemManager().getPluginCopyright(pluginInfo)
        self.dependencies = self.getApp().getPluginSystemManager().getPluginDependencies(pluginInfo)

        #settings = self.getApp().getPluginSystemManager().getPluginSettings(pluginInfo)
        #hasDependencies = self.getApp().getPluginSystemManager().hasPluginDependency(pluginInfo)

        #externalData = self.getApp().getPluginSystemManager().getPluginExternalData(pluginInfo)
        self.helpUri = self.getApp().getPluginSystemManager().getPlugingetHelpUri(pluginInfo)
        self.dataDir = self.getApp().getPluginSystemManager().getPluginDataDir(pluginInfo)
        self.updateTranslationContext()

    def updateTranslationContext(self, domain = None, localeDir = None,  language = None, fallbackToOrcaTranslation = True):
        self.translationContext = None
        useLocaleDir = '{}/locale/'.format(self.getModuleDir())
        if localeDir:
            if os.path.isdir(localeDir):
                useLocaleDir = localeDir
        useName = self.getModuleName()
        useDomain = useName
        if domain:
            useDomain = domain
        useLanguage = None
        if language:
            useLanguage = language
        self.translationContext = self.getApp().getTranslationManager().initTranslation(useName, domain=useDomain, localeDir=useLocaleDir, language=useLanguage, fallbackToOrcaTranslation=fallbackToOrcaTranslation)
        # Point _ to the translation object in the globals namespace of the caller frame
        try:
            callerFrame = inspect.currentframe().f_back
            # Install our gettext and ngettext function to the upper frame
            callerFrame.f_globals['_'] = self.translationContext.gettext
            callerFrame.f_globals['ngettext'] = self.translationContext.ngettext
        finally:
            del callerFrame # Avoid reference problems with frames (per python docs)
    def getTranslationContext(self):
        return self.translationContext
    def isPluginBuildIn(self):
        return self.buildIn
    def isPluginHidden(self):
        return self.hidden
    def getAuthors(self):
        return self.authors
    def getCopyright(self):
        return self.copyright
    def getDataDir(self):
        return self.dataDir
    def getDependencies(self):
        return self.dependencies
    def getDescription(self):
        return self.description
    def getgetHelpUri(self):
        return self.helpUri
    def getIconName(self):
        return self.iconName
    def getModuleDir(self):
        return self.moduleDir
    def getModuleName(self):
        return self.moduleName
    def getName(self):
        return self.name
    def getVersion(self):
        return self.version
    def getWebsite(self):
        return self.website
    def registerGestureByString(self, function, name, gestureString, learnModeEnabled = True):
        keybinding = self.getApp().getAPIHelper().registerGestureByString(self.getModuleName(), function, name, gestureString, 'default', 'orca', learnModeEnabled)
        return keybinding
    def unregisterShortcut(self, function, name, gestureString, learnModeEnabled = True):
        ok = self.getApp().getAPIHelper().unregisterShortcut(self.getModuleName(), keybinding)
        return ok
    def registerSignal(self, signalName, signalFlag = GObject.SignalFlags.RUN_LAST, closure = GObject.TYPE_NONE, accumulator=()):
        ok = self.signalManager.registerSignal(self.getModuleName(), signalName, signalFlag, closure, accumulator)
        return ok
    def unregisterSignal(self, signalName):
        # how to unregister?
        pass

    def connectSignal(self, signalName, function, param = None):
        signalID = self.signalManager.connectSignal(self.getModuleName(), signalName, function, param)
        return signalID
    def disconnectSignalByFunction(self, function):
        # need get mapped function
        mappedFunction = function
        self.signalManager.disconnectSignalByFunction(self.getName(), mappedFunction)

    def registerAPI(self, key, value, application = ''):
        ok = self.dynamicApiManager.registerAPI(key, value, contextName = self.getModuleName(), application = application)
        return ok
    def unregisterAPI(self, key, application = ''):
        self.dynamicApiManager.unregisterAPI(self.getModuleName(), key, application = application)
