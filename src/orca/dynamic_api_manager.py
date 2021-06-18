import gi
from gi.repository import GObject


class DynamicApiManager():
    def __init__(self, app):
        self.app = app
        self.orcaAPI = {'Orca': self.app}
    def registerAPI(self, key, value):
        # add dynamic API
        self.orcaAPI[key] = value
    def unregisterAPI(self, key):
        try:
            del self.orcaAPI[key]
        except:
            print('API Key: "{}" not found,'.format(key))
    def getAPI(self, key):
        # get dynamic API
        return self.orcaAPI.get(key)
