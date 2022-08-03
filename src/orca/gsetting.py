import gi
from gi.repository import GObject, Gio

class Gsetting():
    def __init__(self, app):
        self.app = app
    def loadDefaultSetting(application = '', profile = '', resource = None, schema_id):
        schema_source = Gio.SettingsSchemaSource.new_from_directory('{}/config/'.format(self.getModuleDir()), Gio.SettingsSchemaSource.get_default(), False)
        schema = Gio.SettingsSchemaSource.lookup(schema_source, "org.gnome.orca.GSettingsTest", False)
        setting = Gio.Settings.new_full(schema, None, '/org/chrys/')
    def setSetting(key, value, application = '', profile = '', resource = None, schema_id):
        schema_source = Gio.SettingsSchemaSource.new_from_directory('{}/config/'.format(self.getModuleDir()), Gio.SettingsSchemaSource.get_default(), False)
        schema = Gio.SettingsSchemaSource.lookup(schema_source, "org.gnome.orca.GSettingsTest", False)
        setting = Gio.Settings.new_full(schema, None, '/org/chrys/')

        setting.get_boolean('testbool')

    def initCurrentSettings(settings_path , schema_id, source_directory, profile, application, domain, name = None)
        source_directory = '{}/config/'.format(self.getModuleDir())
        settings_path = '/org/chrys/'
        schema_id = "org.gnome.orca.GSettingsTest"

        schema_source = Gio.SettingsSchemaSource.new_from_directory(source_directory, Gio.SettingsSchemaSource.get_default(), False)
        schema = Gio.SettingsSchemaSource.lookup(schema_source, schema_id, False)
        setting = Gio.Settings.new_full(schema, None, settings_path)
        
        
        '''
        schema_source = Gio.SettingsSchemaSource.new_from_directory('{}/config/'.format(self.getModuleDir()), Gio.SettingsSchemaSource.get_default(), False)
        schema = Gio.SettingsSchemaSource.lookup(schema_source, "org.gnome.orca.GSettingsTest", False)
        setting = Gio.Settings.new_full(schema, None, '/org/chrys/')
        '''
        
        
from gi.repository import GObject, Gio
profile = 'Default'
application = 'firefox'
source_directory = '{}/config/'.format('/home/chrys/.local/share/orca/plugins/gsettingsTest')
settings_path = '/org/chrys/{}/{}/'.format(profile, application)
schema_id = "org.gnome.orca.GSettingsTest"

schema_source = Gio.SettingsSchemaSource.new_from_directory(source_directory, Gio.SettingsSchemaSource.get_default(), False)
schema = Gio.SettingsSchemaSource.lookup(schema_source, schema_id, False)
setting = Gio.Settings.new_full(schema, None, settings_path)
setting.set_boolean('testbool', False)
