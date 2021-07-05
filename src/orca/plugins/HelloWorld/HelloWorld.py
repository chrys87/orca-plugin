from orca import plugin

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
    def do_deactivate(self):
        API = self.object
        print('deactivate hello world plugin')
