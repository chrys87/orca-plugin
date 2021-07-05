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
        pluginInfo = self.getPluginInfo()
        self.moduleDir = self.app.getPluginSystemManager().getPluginModuleDir(pluginInfo)

        self.hidden = self.app.getPluginSystemManager().isPluginHidden(pluginInfo)

        self.moduleName = self.app.getPluginSystemManager().getPluginModuleName(pluginInfo)
        self.name = self.app.getPluginSystemManager().getPluginName(pluginInfo)
        self.version = self.app.getPluginSystemManager().getPluginVersion(pluginInfo)
        self.website = self.app.getPluginSystemManager().getPluginWebsite(pluginInfo)
        self.authors = self.app.getPluginSystemManager().getPluginAuthors(pluginInfo)
        self.buildIn = self.app.getPluginSystemManager().isPluginBuildIn(pluginInfo)
        self.description = self.app.getPluginSystemManager().getPluginDescription(pluginInfo)
        self.iconName = self.app.getPluginSystemManager().getPluginIconName(pluginInfo)
        self.copyright = self.app.getPluginSystemManager().getPluginCopyright(pluginInfo)
        self.dependencies = self.app.getPluginSystemManager().getPluginDependencies(pluginInfo)

        #settings = self.app.getPluginSystemManager().getPluginSettings(pluginInfo)
        #hasDependencies = self.app.getPluginSystemManager().hasPluginDependency(pluginInfo)

        #externalData = self.app.getPluginSystemManager().getPluginExternalData(pluginInfo)
        self.helpUri = self.app.getPluginSystemManager().getPlugingetHelpUri(pluginInfo)
        self.dataDir = self.app.getPluginSystemManager().getPluginDataDir(pluginInfo)
