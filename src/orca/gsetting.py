import gi
from gi.repository import GObject, Gio

class Gsetting():
    def __init__(self, app):
        self.app = app
    def loadSettings():
        pass
    def initSettings(key, application = '', profile = '', resource = None, schema_id = None):
    def getSetting(key, application = '', profile = '', resource = None, schema_id = None):
        pass
    def setSetting(key, value, application = '', profile = '', resource = None, schema_id):
        schema_source = Gio.SettingsSchemaSource.new_from_directory('{}/config/'.format(self.getModuleDir()), Gio.SettingsSchemaSource.get_default(), False)
        schema = Gio.SettingsSchemaSource.lookup(schema_source, "org.gnome.orca.GSettingsTest", False)
        setting = Gio.Settings.new_full(schema, None, '/org/chrys/')

        setting.get_boolean('testbool')
    def resetSetting(key, application = '', profile = '', resource = None, schema_id):
        pass
    def exportSettings():
        pass
    def importSettings():
        pass
    def getSettingDatatype():
        pass
    def getSettingDescription():
        pass
