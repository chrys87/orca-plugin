import gi
from gi.repository import GObject, Gio

class Gsetting():
    def __init__(self, app):
        self.app = app
        self.profileList = []
        self.applicationList = []
        self.base_settings_domain = "org.a11y.orca"
        self.base_settings = Gio.Settings.new(self.base_settings_domain)
        self.base_settings.connect("changed::profiles", self.on_profiles_changed)
        self.base_settings.connect("changed::applications", self.on_applications_changed)
    def on_applications_changed(self, settings, key):
        self.applicationList = list(self.base_settings.get_value('applications'))
    def on_profiles_changed(self, settings, key):
        self.profileList = list(self.base_settings.get_value('profiles'))

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
'''
