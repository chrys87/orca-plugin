from orca import plugin

import gettext
import inspect, os
mypath = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

import gi, time
gi.require_version('Peas', '1.0')
from gi.repository import GObject
from gi.repository import Peas

class HelloWorld(GObject.Object, Peas.Activatable, plugin.Plugin):
    __gtype_name__ = 'helloworld'

    object = GObject.Property(type=GObject.Object)
    def __init__(self):
        plugin.Plugin.__init__(self)
    def do_activate(self):
        API = self.object
        print('activate hello world plugin')
        #for lang in ['es', 'en']:
        print(mypath)
        gt = gettext.translation('base', localedir=mypath+'/locales')
        #el = gettext.translation('base', localedir='locales', languages=['de'])
        gt.install()
        _ = gt.gettext
        print(_("Hello World"))
        print(_("This is a translatable string"))
    def do_deactivate(self):
        API = self.object
        print('deactivate hello world plugin')
