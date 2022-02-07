import gi
from gi.repository import GObject

from orca import resource_manager

class DynamicApiManager():
    def __init__(self, app):
        self.app = app
        self.resourceManager = self.app.getResourceManager()
        self.api = {'Orca': self.app}
    def registerAPI(self, key, value, application = '', contextName = None):
        # add profile
        try:
            d = self.api[application]
        except KeyError: 
            self.api[application]= {}
        # add dynamic API
        self.api[application][key] = value
        resourceContext = self.resourceManager.getResourceContext(contextName)
        if resourceContext:
            resourceEntry = resource_manager.ResourceEntry('api', key, value, value, key)
            resourceContext.addAPI(application, key, resourceEntry)

    def unregisterAPI(self, key,  application = '', contextName = None):
        ok = False
        try:
            del self.api[application][key]
            ok = True
        except:
            print('API Key: "{}/{}" not found,'.format(application, key))
        resourceContext = self.resourceManager.getResourceContext(contextName)
        if resourceContext:
            resourceContext.removeAPI(application, key)
        return ok
    def getAPI(self, key, application = '', fallback = True):
        # get dynamic API
        api = None
        
        try:
            api = self.api[application][key]
            return api
        except:
            if not fallback:
                print('API Key: "{}/{}" not found,'.format(application, key))
                return None

        # we already tried this
        if application == '':
            return api

        try:
            api = self.api[application]['']
        except:
            print('API Key: "{}/{}" not found,'.format(application, key))
        
        return api
