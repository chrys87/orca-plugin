import gi
from gi.repository import GObject

from orca import resource_manager

class DynamicApiManager():
    def __init__(self, app):
        self.app = app
        self.resourceManager = self.app.getResourceManager()
        self.orcaAPI = {'Orca': self.app}
    def registerAPI(self, key, value, contextName = '', application = ''):
        # add profile
        try:
            d = self.orcaAPI[application]
        except KeyError: 
            self.orcaAPI[application]= {}
        # add dynamic API
        self.orcaAPI[application][key] = value
        if contextName:
            resourceContext = self.resourceManager.getResourceContext(contextName)
            if resourceContext:
                resourceEntry = resource_manager.ResourceEntry('api', key, value, value, key)
                resourceContext.addAPI(application, key, resourceEntry)

    def unregisterAPI(self, contextName, key,  application = ''):
        ok = False
        try:
            del self.orcaAPI[application][key]
            ok = True
        except:
            print('API Key: "{}/{}" not found,'.format(application, key))
        if contextName:
            resourceContext = self.resourceManager.getResourceContext(contextName)
            if resourceContext:
                resourceContext.removeAPI(application, key)
        return ok
    def getAPI(self, key, application = '', fallback = True):
        # get dynamic API
        api = None
        
        try:
            api = self.orcaAPI[application][key]
            return api
        except:
            if not fallback:
                print('API Key: "{}/{}" not found,'.format(application, key))
                return None

        # we already tried this
        if application == '':
            return api

        try:
            api = self.orcaAPI[application]['']
        except:
            print('API Key: "{}/{}" not found,'.format(application, key))
        
        return api
