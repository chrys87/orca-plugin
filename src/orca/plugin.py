import gi, time
gi.require_version('Peas', '1.0')
from gi.repository import GObject
from gi.repository import Peas

class Plugin(GObject.Object, Peas.Activatable):
    #__gtype_name__ = 'BasePlugin'

    object = GObject.Property(type=GObject.Object)
    def __init__(self):
        pass
    def do_activate(self):
        API = self.object
    def do_deactivate(self):
        API = self.object
