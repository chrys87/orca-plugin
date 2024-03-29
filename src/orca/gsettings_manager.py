import gi
from gi.repository import GObject, Gio, GLib

GLOBAL_SCHEMA_ID = "org.a11y.orca.global"
PROFILE_SCHEMA_ID = "org.a11y.orca.profile"
SETTINGS_ROOT_PATH = '/org/a11y/orca/'
DEFAULT_PROFILE_NAME = 'default'

class GsettingsManager():
    def __init__(self, app):
        self.app = app
        self.profileList = []
        self.applicationList = []
        self.set_global_settings(self.register_setting(GLOBAL_SCHEMA_ID))
        self.current_profile_settings = None

        self.set_profileList(self.get_settings_value_list('available-profiles', settings=self.get_global_settings()))

        self.set_active_profile(self.get_settings_value_string('active-profile', settings=self.get_global_settings()))
        # try to deactivate
        #self.get_global_settings().connect("changed::profiles", self.on_profiles_changed)
        #self.get_global_settings().connect("changed::active-profile", self.on_active_profile_changed)

    def register_setting(self, schema_id, profile_name = None, application_name =None, plugin_name = None, sub_setting_name = None, source_directory = '', version = 0):
        if profile_name:
            if not profile_name in self.get_profileList():
                profile_name = DEFAULT_PROFILE_NAME
        # get settings path
        #if not settings_path:
        settings_path = SETTINGS_ROOT_PATH
        if profile_name:
            settings_path += 'profiles/{}/'.format(profile_name)
        if application_name:
            if application_name in self.applicationList:
                settings_path += 'applications/{}/'.format(application_name)
        if plugin_name:
            settings_path += 'plugins/{}/'.format(plugin_name)
        if sub_setting_name:
            settings_path += 'settings/{}/'.format(sub_setting_name)
            
        settings = None
        if schema_id in (GLOBAL_SCHEMA_ID, PROFILE_SCHEMA_ID):
            settings = Gio.Settings(schema_id, settings_path)
        else:
            if source_directory == '':
                return settings
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
        self.set_settings_value_list('available-profiles', newProfileList, settings=self.get_global_settings())

    def remove_profile(self, profile = ''):
        if profile in ['', DEFAULT_PROFILE_NAME]:
            return
        newProfileList = self.get_profileList().copy()
        if not profile in newProfileList:
            return
        newProfileList.remove(profile)
        self.set_settings_value_list('available-profiles', newProfileList, settings=self.get_global_settings())
        # remove everything under profile folder recursive here
    def add_application(self, application = ''):
        if application == '':
            return
        newApplicationList = self.get_applicationList().copy()
        if application in newApplicationList:
            return
        newApplicationList.append(application)
        self.set_settings_value_list(self.get_current_profile_settings(), 'application-settings', newApplicationList, settings=self.get_global_settings())

    def remove_application(self, application = ''):
        if application == '':
            return
        newApplicationList = self.get_applicationList().copy()
        if not application in newApplicationList:
            return
        newApplicationList.remove(application)
        self.set_settings_value_list(self.get_current_profile_settings(), 'application-settings', newApplicationList, settings=self.get_global_settings())
        # remove everything under application folder recursive here

    def on_applications_changed(self, settings, key):
        self.set_applicationList(self.get_settings_value_list(key))

    def set_applicationList(self, new_applicationList):
        self.applicationList = new_applicationList
        print('available-applications: ' + str(self.get_applicationList()))

    def get_applicationList(self):
        return self.applicationList

    def on_profiles_changed(self, settings, key):
        self.set_profileList(self.get_settings_value_list(key), settings=self.get_global_settings())
        if not DEFAULT_PROFILE_NAME in self.get_settings_value_list(key, settings=self.get_global_settings()):
            self.add_profile(DEFAULT_PROFILE_NAME)
        self.set_profileList(self.get_settings_value_list(key, settings=self.get_global_settings()))
        if not self.get_settings_value_string('active-profile', settings=self.get_global_settings()) in self.get_settings_value_list(key, settings=self.get_global_settings()):
            self.set_active_profile(DEFAULT_PROFILE_NAME)
        self.set_profileList(self.get_settings_value_list(key, settings=self.get_global_settings()))
    def on_active_profile_changed(self, settings, key):
        self.set_active_profile(self.get_settings_value_string( key, settings=self.get_global_settings()))
        
    def set_active_profile(self, new_active_profile):
        if not DEFAULT_PROFILE_NAME in self.get_profileList():
            self.add_profile(DEFAULT_PROFILE_NAME)
        if not new_active_profile in self.get_profileList():
            new_active_profile = DEFAULT_PROFILE_NAME

        # disconnect here self.get_current_profile_settings.d("changed::application-settings", self.on_applications_changed)
        self.set_current_profile_settings( self.register_setting(PROFILE_SCHEMA_ID, profile_name = new_active_profile))

        if new_active_profile != self.get_settings_value_string('active-profile', settings=self.get_global_settings()):
            print('active profile: ' + new_active_profile)
            self.set_settings_value_string('active-profile', new_active_profile, settings=self.get_global_settings())

    def set_profileList(self, new_profileList):
        self.profileList = new_profileList
        print('available profiles: ' + str(self.get_profileList()))

    def get_profileList(self):
        return self.profileList
    
    def getSettingsForScope(self, settings = None, profile_name = None, application_name =None, plugin_name = None):
        # if a settings instance is given, force that
        if settings:
            return settings
        usedSettings = None
        # otherwhise search:
        # 1. application scope
        # 2. global profile settings

        # TODO: search here for per application settings
        if not usedSettings:
            usedSettings = self.get_current_profile_settings()
                
        return usedSettings

    # value
    def get_settings_value(self, key, settings = None, profile_name = None, application_name =None, plugin_name = None):
        settings = self.getSettingsForScope(settings, profile_name, application_name, plugin_name)
        return settings.get_value(key)
    def set_settings_value(self, key, value, format = '', settings = None, profile_name = None, application_name =None, plugin_name = None):
        settings = self.getSettingsForScope(settings, profile_name, application_name, plugin_name)
        if format != '':
            value = GLib.Variant(format, value)
        settings.set_value(key, value)

    # string
    def get_settings_value_string(self, key, settings = None, profile_name = None, application_name =None, plugin_name = None):
        settings = self.getSettingsForScope(settings, profile_name, application_name, plugin_name)
        return settings.get_string(key)
    def set_settings_value_string(self, key, value, settings = None, profile_name = None, application_name =None, plugin_name = None):
        settings = self.getSettingsForScope(settings, profile_name, application_name, plugin_name)
        settings.set_string(key, value)

    # int
    def get_settings_value_int(self, key, settings = None, profile_name = None, application_name =None, plugin_name = None):
        settings = self.getSettingsForScope(settings, profile_name, application_name, plugin_name)
        return settings.get_int(key)
    def set_settings_value_int(self, key, value, settings = None, profile_name = None, application_name =None, plugin_name = None):
        settings = self.getSettingsForScope(settings, profile_name, application_name, plugin_name)
        settings.set_int(key, value)

    # bool
    def get_settings_value_boolean(self, key, settings = None, profile_name = None, application_name =None, plugin_name = None):
        settings = self.getSettingsForScope(settings, profile_name, application_name, plugin_name)
        return settings.get_boolean(key)
    def set_settings_value_boolean(self, key, value, settings = None, profile_name = None, application_name =None, plugin_name = None):
        settings = self.getSettingsForScope(settings, profile_name, application_name, plugin_name)
        settings.set_boolean(key, value)

    # list
    def get_settings_value_list(self, key, settings = None, profile_name = None, application_name =None, plugin_name = None):
        settings = self.getSettingsForScope(settings, profile_name, application_name, plugin_name)
        return list(settings.get_value(key))
    def set_settings_value_list(self, key, value, format = 'as', settings = None, profile_name = None, application_name =None, plugin_name = None):
        '''
        as = array string
        ai = array integer
        ab = array boolean
        '''
        settings = self.getSettingsForScope(settings, profile_name, application_name, plugin_name)
        self.set_settings_value(key, value, format=format, settings = settings, profile_name = profile_name, application_name =application_name, plugin_name = plugin_name)

    def get_global_settings(self):
        return self.global_settings
    def set_global_settings(self, new_global_settings):
        self.global_settings = new_global_settings
        self.get_global_settings().connect("changed::profiles", self.on_profiles_changed)
        self.get_global_settings().connect("changed::active-profile", self.on_active_profile_changed)
    def get_current_profile_settings(self):
        return self.current_profile_settings
    def set_current_profile_settings(self, new_profile_settings):
        self.current_profile_settings = new_profile_settings
        self.current_profile_settings.connect("changed::application-settings", self.on_applications_changed)

        self.set_applicationList(self.get_settings_value_list('application-settings', settings=self.current_profile_settings))

        self.current_profile_settings.set_int('profile-version', self.current_profile_settings.get_int('profile-version'))
        self.set_settings_value_list('application-settings', self.get_applicationList(), settings=self.current_profile_settings)

