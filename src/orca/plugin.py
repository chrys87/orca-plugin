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

    def setApp(self, app):
        self.app = app
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
