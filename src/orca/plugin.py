class Plugin():
    #__gtype_name__ = 'BasePlugin'

    def __init__(self):
        self.API = None
    def setAPI(self, API):
        self.API = API
    def getAPI(self):
        return self.API

