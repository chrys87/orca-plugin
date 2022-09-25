import gi
from gi.repository import GObject, Gio, GLib

GLOBAL_SCHEMA_ID = "org.a11y.orca.global"
SETTINGS_ROOT_PATH = '/org/a11y/orca/'
DEFAULT_PROFILE_NAME = 'default'

class GsettingsManager():
    def __init__(self, app):
        self.app = app
        self.profileList = []
        self.applicationList = []
        self.global_settings = self.register_setting(GLOBAL_SCHEMA_ID)
        #self.register_setting('org.gnome.orca.GSettingsTest', profile = 'testprofile', application = 'testapp', domain = 'testdomain', source_directory = '/home/chrys/Projekte/orca-plugins/gsettingsTest/config/')
        #self.register_setting('org.gnome.orca.GSettingsTest', profile = 'testprofile2', application = 'testapp', domain = 'testdomain', source_directory = '/home/chrys/Projekte/orca-plugins/gsettingsTest/config/')
        #self.register_setting('org.gnome.orca.GSettingsTest', profile = 'testprofile', application = 'testapp2', domain = 'testdomain', source_directory = '/home/chrys/Projekte/orca-plugins/gsettingsTest/config/')
        #self.register_setting('org.gnome.orca.GSettingsTest', profile = 'testprofile', application = 'testapp2', domain = 'testdomain2', source_directory = '/home/chrys/Projekte/orca-plugins/gsettingsTest/config/')

        self.set_profileList(self.get_global_settings_value_list('available-profiles'))
        #self.set_applicationList(self.get_global_settings_value_list('available-applications'))
        #self.global_settings.connect("changed::applications", self.on_applications_changed)

        self.set_active_profile(self.get_global_settings_value_string('active-profile'))
        self.global_settings.connect("changed::profiles", self.on_profiles_changed)
        self.global_settings.connect("changed::active-profile", self.on_active_profile_changed)
    def register_setting(self, schema_id, profile_name = None, application_name =None, plugin_name = None, sub_setting_name = None, source_directory = ''):
        # get settings path
        settings_path = SETTINGS_ROOT_PATH
        if profile_name:
            settings_path += 'profiles/{}/'.format(profile_name)
        if application_name:
            settings_path += 'applications/{}/'.format(application_name)
        if plugin_name:
            settings_path += 'plugins/{}/'.format(plugin_name)
        if sub_setting_name:
            settings_path += 'settings/{}/'.format(sub_setting_name)
            
        settings = None
        if schema_id == GLOBAL_SCHEMA_ID:
            settings = Gio.Settings(schema_id, settings_path)
        else:
            schema_source = Gio.SettingsSchemaSource.new_from_directory(source_directory, Gio.SettingsSchemaSource.get_default(), False)
            schema = Gio.SettingsSchemaSource.lookup(schema_source, schema_id, False)
            settings = Gio.Settings.new_full(schema, None, settings_path)
            #settings.set_boolean('testbool', False)

        #self.settingDict = {profile: {application:{domain:settings}}}
        # resource manager here

        return settings
    def add_profile(self, profile = ''):
        if profile == '':
            return
        newProfileList = self.get_profileList().copy()
        if profile in newProfileList:
            return
        newProfileList.append(profile)
        self.set_global_settings_value_list('available-profiles', newProfileList)

    def remove_profile(self, profile = ''):
        if profile in ['', DEFAULT_PROFILE_NAME]:
            return
        newProfileList = self.get_profileList().copy()
        if not profile in newProfileList:
            return
        newProfileList.remove(profile)
        self.set_global_settings_value_list('available-profiles', newProfileList)
    '''
    def add_application(self, application = ''):
        if application == '':
            return
        newApplicationList = self.get_applicationList().copy()
        if application in newApplicationList:
            return
        newApplicationList.append(application)
        self.set_global_settings_value_list('available-applications', newApplicationList)

    def remove_application(self, application = ''):
        if application == '':
            return
        newApplicationList = self.get_applicationList().copy()
        if not application in newApplicationList:
            return
        newApplicationList.remove(application)
        self.set_global_settings_value_list('available-applications', newApplicationList)

    def on_applications_changed(self, settings, key):
        self.applicationList(self.get_global_settings_value_list(key))

    def set_applicationList(self, new_applicationList):
        self.applicationList = new_applicationList
        print('available-applications: ' + str(self.get_applicationList()))

    def get_applicationList(self):
        return self.applicationList
    '''

    def on_profiles_changed(self, settings, key):
        self.set_profileList(self.get_global_settings_value_list(key))
        if not DEFAULT_PROFILE_NAME in self.get_global_settings_value_list(key):
            self.add_profile(DEFAULT_PROFILE_NAME)
        self.set_profileList(self.get_global_settings_value_list(key))
        if not self.get_global_settings_value_string('active-profile') in self.get_global_settings_value_list(key):
            self.set_active_profile(DEFAULT_PROFILE_NAME)
        self.set_profileList(self.get_global_settings_value_list(key))
    def on_active_profile_changed(self, settings, key):
        self.set_active_profile(self.get_global_settings_value_string(key))
        
    def set_active_profile(self, new_active_profile):
        if not DEFAULT_PROFILE_NAME in self.get_profileList():
            self.add_profile(DEFAULT_PROFILE_NAME)
        if not new_active_profile in self.get_profileList():
            new_active_profile = DEFAULT_PROFILE_NAME
        if new_active_profile != self.get_global_settings_value_string('active-profile'):
            print('active profile: ' + new_active_profile)
            self.set_global_settings_value_string('active-profile', new_active_profile)

    def set_profileList(self, new_profileList):
        self.profileList = new_profileList
        print('available profiles: ' + str(self.get_profileList()))

    def get_profileList(self):
        return self.profileList

    # value
    def get_global_settings_value(self, key):
        return self.get_global_settings().get_value(key)
    def set_global_settings_value(self, key, value, format = ''):
        if format != '':
            value = GLib.Variant(format, value)
        self.get_global_settings().set_value(key, value)


    # string
    def get_global_settings_value_string(self, key):
        return self.get_global_settings().get_string(key)
    def set_global_settings_value_string(self, key, value):
        self.get_global_settings().set_string(key, value)

    # int
    def get_global_settings_value_int(self, key):
        return self.get_global_settings().get_int(key)
    def set_global_settings_value_int(self, key, value):
        self.get_global_settings().set_int(key, value)

    # bool
    def get_global_settings_value_boolean(self, key):
        return self.get_global_settings().get_boolean(key)
    def set_global_settings_value_boolean(self, key, value):
        self.get_global_settings().set_boolean(key, value)
    # list
    def get_global_settings_value_list(self, key):
        return list(self.get_global_settings().get_value(key))
    def set_global_settings_value_list(self, key, value, format = 'as'):
        '''
        as = array string
        ai = array integer
        ab = array boolean
        '''
        self.set_global_settings_value(key, value, format)

    def get_global_settings(self):
        return self.global_settings
    
'''
    def exportAllSettings():
        pass
    def importSettings():
        pass
    def installSettings():
        pass
    def uninstallSettings():
        pass
'''


