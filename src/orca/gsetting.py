import gi
from gi.repository import GObject

class Gsetting():
    def __init__(self, app):
        self.app = app
        self.api = {'Orca': self.app} 
    def loadSettings():
        pass
    def getSetting(key, application = '', profile = ''):
        pass
    def setSetting(key, value, application = '', profile = ''):
        pass
    def resetSetting(key, application = '', profile = ''):
        pass
    def exportSettings():
        pass
    def importSettings():
        pass
    def getSettingDatatype():
        pass
    def getSettingDescription():
        pass
